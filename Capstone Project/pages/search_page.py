"""
Page Object for the header search box and search-results listing.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    PRODUCT_RESULT_CARDS = (By.CSS_SELECTOR, ".product-layout")
    PRODUCT_TITLE_LINKS = (By.CSS_SELECTOR, ".product-layout .caption h4 a")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[onclick*='cart.add']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")

    def search_product(self, term: str):
        self.type_text(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)

    def has_results(self) -> bool:
        return self.is_visible(self.PRODUCT_RESULT_CARDS, timeout=8)

    def get_first_product_name(self) -> str:
        return self.find_all(self.PRODUCT_TITLE_LINKS)[0].text

    def add_first_result_to_cart(self):
        buttons = self.find_all(self.ADD_TO_CART_BUTTONS)
        buttons[0].click()

    def wait_for_add_to_cart_confirmation(self) -> bool:
        return self.is_visible(self.SUCCESS_ALERT, timeout=10)
