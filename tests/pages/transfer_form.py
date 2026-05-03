from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TransferForm:
    CARD_INPUT = (By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']")
    AMOUNT_INPUT = (By.CSS_SELECTOR, "input[placeholder='1000']")
    COMMISSION = (By.ID, "comission")
    TRANSFER_BUTTON = (By.XPATH, "//button[.//span[text()='Перевести']]")
    INSUFFICIENT_FUNDS = (By.XPATH, "//span[contains(text(),'Недостаточно средств')]")

    def __init__(self, driver):
        self.driver = driver

    def enter_card_number(self, text: str) -> "TransferForm":
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CARD_INPUT)
        )
        field.clear()
        field.send_keys(text)
        return self

    def enter_amount(self, text) -> "TransferForm":
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.AMOUNT_INPUT)
        )
        # Поле amount имеет defaultValue=1000, поэтому простой send_keys дописывает в конец.
        # Через native setter + dispatch input аккуратно заменяем значение целиком.
        self.driver.execute_script(
            "const setter = Object.getOwnPropertyDescriptor("
            "window.HTMLInputElement.prototype, 'value').set;"
            "setter.call(arguments[0], arguments[1]);"
            "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
            field,
            str(text),
        )
        return self

    def card_input_value_digits(self) -> str:
        value = self.driver.find_element(*self.CARD_INPUT).get_attribute("value") or ""
        return value.replace(" ", "")

    def commission_text(self) -> str:
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.COMMISSION)
        )
        return element.text

    def is_transfer_button_present(self, timeout: float = 2.0) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.TRANSFER_BUTTON)
            )
            return True
        except TimeoutException:
            return False

    def click_transfer_and_get_alert_text(self) -> str:
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.TRANSFER_BUTTON)
        )
        # JS click обходит проблему фокуса в headless Chrome,
        # из-за которой нативные alerts иногда не всплывают через обычный click().
        self.driver.execute_script("arguments[0].click();", button)
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text

    def error_message_text(self, timeout: float = 5.0) -> str:
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.INSUFFICIENT_FUNDS)
        )
        return element.text

    def take_screenshot(self, path: str) -> "TransferForm":
        self.driver.save_screenshot(path)
        return self
