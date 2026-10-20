from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SearchPage:
    URL = "https://demo-opencart.ru/index.php?route=common/home"

    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[name="search"].input-lg')
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.btn-default.btn-lg")
    PRODUCT_LINKS = (
        By.XPATH,
        '//a[contains(@href, "route=product/product") and normalize-space(.) != ""]',
    )

    EMPTY_MESSAGE = (
        By.XPATH,
        '//*[normalize-space(.) = "Нет товаров, которые соответствуют критериям поиска."]',
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def search(self, query):
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(query)

        search_button = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )
        search_button.click()

        self.wait.until(EC.staleness_of(search_input))

    def get_product_names(self):
        links = self.wait.until(
            EC.visibility_of_all_elements_located(self.PRODUCT_LINKS)
        )
        return [link.text.strip() for link in links]

    def get_empty_message(self):
        message = self.wait.until(
            EC.visibility_of_element_located(self.EMPTY_MESSAGE)
        )
        return message.text.strip()

    def get_product_count(self):
        links = self.driver.find_elements(*self.PRODUCT_LINKS)
        return len(links)