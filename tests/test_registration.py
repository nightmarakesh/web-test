from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.registration_page import RegistrationPage


def test_registration_success(driver):
    """Цель: зарегистрировать пользователя и проверить подтверждение."""
    email = f"selenium_{uuid4().hex}@example.com"
    password = "TestOnly_826491!"

    page = RegistrationPage(driver)
    page.open()
    page.register(email, password)

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.url_contains("route=account/success")
    )

    assert "route=account/success" in driver.current_url, (
        f"Unexpected URL: {driver.current_url}"
    )

    confirmation = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#content > h1")
        )
    )

    actual_text = confirmation.text
    expected_text = "Ваша учетная запись создана!"


    assert actual_text == expected_text, (
        f"Unexpected confirmation text. "
        f"Actual: {ascii(actual_text)}. "
        f"Expected: {ascii(expected_text)}"
    )


def test_registration_with_existing_email(driver):
    """Цель: отклонить повторную регистрацию уже зарегистрированного email."""
    email = f"duplicate_{uuid4().hex}@example.com"
    password = "TestOnly_826491!"

    page = RegistrationPage(driver)
    wait = WebDriverWait(driver, 10)

    page.open()
    page.register(email, password)

    wait.until(
        EC.url_contains("route=account/success")
    )

    driver.delete_all_cookies()

    page.open()

    wait.until(
        EC.visibility_of_element_located(
            (By.ID, "input-email")
        )
    )

    page.register(email, password)

    actual_message = page.get_error_message()
    expected_message = "Данный E-Mail уже зарегистрирован!"

    assert actual_message == expected_message, (
        f"Unexpected error message. "
        f"Actual: {ascii(actual_message)}. "
        f"Expected: {ascii(expected_message)}"
    )

    assert "route=account/register" in driver.current_url, (
        f"Unexpected URL after duplicate registration: {driver.current_url}"
    )