"""
End-to-end test: launch -> login/register -> search -> add to cart ->
update quantity -> verify cart -> report.

Each step is wrapped so that a failure is recorded (with a screenshot)
in the HTML report rather than silently aborting the whole run, and
each step also takes a "success" screenshot when it completes.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import config
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from utils.driver_factory import DriverFactory
from utils.data_reader import get_test_data
from utils.screenshot_utils import capture_screenshot
from utils.alert_handler import handle_js_alert_if_present
from utils.report_generator import ReportGenerator


class TestEcommerceFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = get_test_data()
        cls.report = ReportGenerator()
        cls.driver = DriverFactory.get_driver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        report_path = cls.report.generate()
        print(f"\nExecution report generated at: {report_path}")

    def _step(self, name, action, verify_message="OK"):
        """Runs one step, records PASS/FAIL + a screenshot either way."""
        try:
            action()
            shot = capture_screenshot(self.driver, name)
            self.report.add_step(name, "PASS", verify_message, shot)
        except Exception as exc:
            shot = capture_screenshot(self.driver, f"{name}_FAILURE")
            self.report.add_step(name, "FAIL", str(exc), shot)
            raise

    def test_purchase_flow(self):
        driver = self.driver
        user = self.data["user"]
        product = self.data["product"]

        login_page = LoginPage(driver)
        search_page = SearchPage(driver)
        cart_page = CartPage(driver)

        # 1. Launch browser / open application
        self._step(
            "01_launch_application",
            lambda: driver.get(config.BASE_URL),
            f"Opened {config.BASE_URL}",
        )
        handle_js_alert_if_present(driver)

        # 2. Login (falls back to registration on first run)
        self._step(
            "02_login_to_application",
            lambda: login_page.login_or_register(user),
            f"Logged in / registered as {user['email']}",
        )
        self.assertTrue(
            login_page.is_logged_in_or_registered(),
            "Login/registration did not land on an account page",
        )

        # 3. Search product
        self._step(
            "03_search_product",
            lambda: search_page.search_product(product["search_term"]),
            f"Searched for '{product['search_term']}'",
        )
        self.assertTrue(search_page.has_results(), "No search results returned")

        found_product_name = search_page.get_first_product_name()

        # 4. Add product to cart
        self._step(
            "04_add_product_to_cart",
            lambda: search_page.add_first_result_to_cart(),
            f"Added '{found_product_name}' to cart",
        )
        self.assertTrue(
            search_page.wait_for_add_to_cart_confirmation(),
            "Add-to-cart success banner never appeared",
        )
        handle_js_alert_if_present(driver)

        # 5. Update quantity
        def _go_to_cart_and_update():
            cart_page.open_cart()
            cart_page.update_quantity(product["updated_quantity"])

        self._step(
            "05_update_quantity",
            _go_to_cart_and_update,
            f"Updated quantity to {product['updated_quantity']}",
        )

        # 6. Verify cart details
        result_holder = {}

        def _verify():
            result_holder["result"] = cart_page.verify_cart_details(
                found_product_name, product["updated_quantity"]
            )

        self._step(
            "06_verify_cart_details",
            _verify,
            "Verified product name and quantity in cart",
        )
        result = result_holder["result"]
        self.assertTrue(result["name_matches"], f"Cart product mismatch: {result}")
        self.assertTrue(result["quantity_matches"], f"Cart quantity mismatch: {result}")


if __name__ == "__main__":
    unittest.main()
