from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RegistrationPage:
    URL = "https://demo-opencart.ru/index.php?route=account/register"

    AGREE = (By.NAME, "agree")
    SUBMIT = (By.CSS_SELECTOR, 'input[type="submit"][value="Продолжить"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def register(self, email, password):
        fields = {
            "input-firstname": "Test",
            "input-lastname": "Student",
            "input-email": email,
            "input-telephone": "0000000000",
            "input-password": password,
            "input-confirm": password,
        }

        for field_id, value in fields.items():
            field = self.wait.until(
                EC.visibility_of_element_located((By.ID, field_id))
            )
            field.clear()
            field.send_keys(value)

        checkbox = self.wait.until(
            EC.element_to_be_clickable(self.AGREE)
        )

        if not checkbox.is_selected():
            checkbox.click()

        submit_button = self.wait.until(
            EC.element_to_be_clickable(self.SUBMIT)
        )
        submit_button.click()

    def get_error_message(self):
        error = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.alert.alert-danger")
            )
        )
        return error.text.strip()