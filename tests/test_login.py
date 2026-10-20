import os

from pathlib import Path
from uuid import uuid4
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage


def test_login_with_invalid_credentials(driver):
    """Цель: отклонить неверные данные. Ожидаются ошибка и сохранение страницы входа."""
    email = f"unknown_{uuid4().hex}@example.com"

    page = LoginPage(driver)
    page.open()
    page.login(email, "WrongPassword_826491!")

    actual_message = page.get_error_message()
    expected_message = "Неправильно заполнены поле E-Mail и/или пароль!"

    assert actual_message == expected_message, (
        f"Ожидалось: {expected_message!r}. Получено: {actual_message!r}"
    )

    assert "route=account/login" in driver.current_url, (
        f"После неверных данных открыт неожиданный адрес: {driver.current_url}"
    )

def test_login_success(driver):
    """Цель: после входа открыть личный кабинет и увидеть ссылку выхода."""
    email = os.getenv("OPENCART_TEST_EMAIL")
    password = os.getenv("OPENCART_TEST_PASSWORD")

    assert email and password, (
        "Test setup error: OPENCART_TEST_EMAIL and "
        "OPENCART_TEST_PASSWORD must be configured."
    )

    page = LoginPage(driver)
    page.open()
    page.login(email, password)

    logout_locator = (
        By.CSS_SELECTOR,
        'a[href*="route=account/logout"]',
    )

    try:
        WebDriverWait(driver, 10).until(
            lambda browser: (
                "route=account/account" in browser.current_url
                and any(
                    element.is_displayed()
                    for element in browser.find_elements(*logout_locator)
                )
            )
        )
    except TimeoutException:
        artifacts = Path("artifacts")
        artifacts.mkdir(exist_ok=True)

        screenshot = artifacts / "login_success_failed.png"
        driver.save_screenshot(str(screenshot))

        errors = [
            element.text
            for element in driver.find_elements(
                By.CSS_SELECTOR, "div.alert.alert-danger"
            )
            if element.is_displayed()
        ]

        pytest.fail(
            "Expected authentication signs were not found within 10 seconds. "
            f"Current URL: {driver.current_url}. "
            f"Visible errors: {ascii(errors)}. "
            f"Screenshot: {screenshot}",
            pytrace=False,
        )