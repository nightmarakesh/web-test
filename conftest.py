import os

import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    os.environ["SE_SKIP_DRIVER_IN_PATH"] = "true"
    browser = webdriver.Chrome()

    try:
        browser.set_page_load_timeout(30)
        browser.maximize_window()
        yield browser
    finally:
        browser.quit()