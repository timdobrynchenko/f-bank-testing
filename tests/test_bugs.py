from pathlib import Path

from tests.pages.main_page import MainPage

SCREENSHOTS_DIR = Path(__file__).parent.parent / "docs" / "bug-reports" / "screenshots"


def test_commission_is_calculated_with_floor_rounding(driver, base_url):
    form = (
        MainPage(driver, base_url)
        .open(balance=100, reserved=0)
        .click_rub_card()
    )
    form.enter_card_number("1234567890123456")
    form.take_screenshot(str(SCREENSHOTS_DIR / "bug-01-step-3-form-ready.png"))

    form.enter_amount(91)
    form.take_screenshot(str(SCREENSHOTS_DIR / "bug-01-step-4-commission-zero.png"))

    actual = form.commission_text()
    assert actual == "9", (
        f"Ожидалась комиссия 9 руб. для суммы 91 (floor(91*0.1)=9), получено: '{actual}'. "
        f"Баг #1: формула floor(O/100)*10 округляет до десятков рублей вместо рублей."
    )


def test_negative_amount_is_rejected(driver, base_url):
    form = (
        MainPage(driver, base_url)
        .open(balance=100, reserved=0)
        .click_rub_card()
    )
    form.enter_card_number("1234567890123456")
    form.take_screenshot(str(SCREENSHOTS_DIR / "bug-02-step-3-form-ready.png"))

    form.enter_amount("-100")
    form.take_screenshot(str(SCREENSHOTS_DIR / "bug-02-step-4-negative-amount.png"))

    assert not form.is_transfer_button_present(timeout=2.0), (
        "Кнопка 'Перевести' не должна появляться при отрицательной сумме перевода. "
        "Баг #2: обработчик не проверяет amount < 0, отрицательные значения проходят валидацию."
    )


def test_card_number_length_is_limited_to_16(driver, base_url):
    form = (
        MainPage(driver, base_url)
        .open(balance=30000, reserved=0)
        .click_rub_card()
    )
    form.take_screenshot(str(SCREENSHOTS_DIR / "bug-03-step-2-empty-input.png"))

    form.enter_card_number("12345678901234567")
    form.take_screenshot(str(SCREENSHOTS_DIR / "bug-03-step-3-17-digits.png"))

    digits = form.card_input_value_digits()
    assert len(digits) == 16, (
        f"Поле номера карты должно содержать ровно 16 цифр, фактически: {len(digits)} ('{digits}'). "
        f"Баг #3: условие отсечения L.length > 17 пропускает значения длиной 17."
    )
