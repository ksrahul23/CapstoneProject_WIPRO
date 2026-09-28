"""
Page Object for the shopping cart page: quantity update and line-item
verification.
"""

import os
import sys
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from selenium.webdriver.common.by import By

from config import config
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_URL = config.BASE_URL + "index.php?route=checkout/cart"

    CART_ROWS = (By.CSS_SELECTOR, "table.table tbody tr")
    QUANTITY_INPUTS = (By.CSS_SELECTOR, "input[name^='quantity']")
    UPDATE_BUTTONS = (By.CSS_SELECTOR, "button[data-original-title='Update']")
    PRODUCT_NAME_LINKS = (By.CSS_SELECTOR, "table.table tbody tr td a")
    ROW_TOTAL_CELLS = (By.CSS_SELECTOR, "table.table tbody tr td:last-child")
    CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, "#content p")

    def open_cart(self):
        self.open(self.CART_URL)

    def get_row_count(self) -> int:
        return len(self.find_all(self.CART_ROWS))

    def update_quantity(self, new_quantity: int, row_index: int = 0):
        qty_input = self.find_all(self.QUANTITY_INPUTS)[row_index]
        qty_input.clear()
        qty_input.send_keys(str(new_quantity))
        self.find_all(self.UPDATE_BUTTONS)[row_index].click()
        # OpenCart reloads the cart totals via AJAX after an update.
        time.sleep(2)

    def get_product_name(self, row_index: int = 0) -> str:
        return self.find_all(self.PRODUCT_NAME_LINKS)[row_index].text.strip()

    def get_quantity_value(self, row_index: int = 0) -> str:
        return self.find_all(self.QUANTITY_INPUTS)[row_index].get_attribute("value")

    def get_row_total(self, row_index: int = 0) -> str:
        return self.find_all(self.ROW_TOTAL_CELLS)[row_index].text.strip()

    def verify_cart_details(self, expected_name: str, expected_quantity: int) -> dict:
        """Returns a dict of {check_name: bool} for the report/test to
        assert against and log."""
        actual_name = self.get_product_name()
        actual_quantity = self.get_quantity_value()
        return {
            "name_matches": expected_name.lower() in actual_name.lower(),
            "quantity_matches": str(actual_quantity) == str(expected_quantity),
            "actual_name": actual_name,
            "actual_quantity": actual_quantity,
        }
