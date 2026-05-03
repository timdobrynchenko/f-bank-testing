from tests.pages.main_page import MainPage


def test_successful_transfer_shows_alert(driver, base_url):
    form = (
        MainPage(driver, base_url)
        .open(balance=30000, reserved=20001)
        .click_rub_card()
    )
    form.enter_card_number("1234567890123456")
    form.enter_amount(1000)

    alert_text = form.click_transfer_and_get_alert_text()

    assert "Перевод 1000" in alert_text, (
        f"Ожидалось упоминание 'Перевод 1000' в тексте alert, получено: '{alert_text}'."
    )
    assert "принят банком" in alert_text, (
        f"Ожидалось подтверждение 'принят банком' в тексте alert, получено: '{alert_text}'."
    )
    assert "1234567890123456" in alert_text, (
        f"Ожидалось упоминание номера карты 1234567890123456 в тексте alert, получено: '{alert_text}'."
    )


def test_insufficient_funds_message_appears(driver, base_url):
    form = (
        MainPage(driver, base_url)
        .open(balance=30000, reserved=20001)
        .click_rub_card()
    )
    form.enter_card_number("1234567890123456")
    form.enter_amount(10000)

    error = form.error_message_text()

    assert "Недостаточно средств" in error, (
        f"Ожидалось сообщение 'Недостаточно средств', получено: '{error}'."
    )
    assert not form.is_transfer_button_present(timeout=2.0), (
        "Кнопка 'Перевести' не должна отображаться при недостатке средств."
    )
