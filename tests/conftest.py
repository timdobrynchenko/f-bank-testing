import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def base_url() -> str:
    return "http://localhost:8000"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    options.unhandled_prompt_behavior = "ignore"

    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()
