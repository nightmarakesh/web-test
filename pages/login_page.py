from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    URL = "https://demo-opencart.ru/index.php?route=account/login"

    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    SUBMIT = (By.CSS_SELECTOR, 'input[type="submit"][value="Войти"]')
    ERROR = (By.CSS_SELECTOR, "div.alert.alert-danger")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def login(self, email, password):
        email_field = self.wait.until(
            EC.visibility_of_element_located(self.EMAIL)
        )
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD)
        )
        password_field.clear()
        password_field.send_keys(password)

        submit_button = self.wait.until(
            EC.element_to_be_clickable(self.SUBMIT)
        )
        submit_button.click()

        self.wait.until(EC.staleness_of(email_field))

    def get_error_message(self):
        error = self.wait.until(
            EC.visibility_of_element_located(self.ERROR)
        )
        return error.text.strip()