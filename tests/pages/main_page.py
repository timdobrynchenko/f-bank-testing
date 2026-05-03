from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.transfer_form import TransferForm


class MainPage:
    RUB_BALANCE = (By.ID, "rub-sum")
    RUB_RESERVED = (By.ID, "rub-reserved")
    RUB_CARD = (By.XPATH, "//h2[text()='Рубли']/..")

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url

    def open(self, balance: int, reserved: int) -> "MainPage":
        url = f"{self.base_url}/?balance={balance}&reserved={reserved}"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.RUB_BALANCE)
        )
        return self

    def rub_balance_text(self) -> str:
        return self.driver.find_element(*self.RUB_BALANCE).text

    def rub_reserved_text(self) -> str:
        return self.driver.find_element(*self.RUB_RESERVED).text

    def click_rub_card(self) -> TransferForm:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.RUB_CARD)
        ).click()
        return TransferForm(self.driver)
