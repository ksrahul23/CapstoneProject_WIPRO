"""
Base class every Page Object inherits from. Centralizes explicit waits
so individual page classes stay short and only contain locators + the
actions specific to that page.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text: str):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator, timeout: int = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def switch_to_frame_if_present(self, locator):
        try:
            frame = self.find(locator)
            self.driver.switch_to.frame(frame)
            return True
        except Exception:
            return False
