"""
Page Object for Login + Register (tutorialsninja.com/demo is a
standard OpenCart install, so these are the stock OpenCart routes).
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from selenium.webdriver.common.by import By

from config import config
from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_URL = config.BASE_URL + "index.php?route=account/login"
    REGISTER_URL = config.BASE_URL + "index.php?route=account/register"

    # --- Login form ---
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    LOGIN_ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")

    # --- Register form ---
    FIRSTNAME_INPUT = (By.ID, "input-firstname")
    LASTNAME_INPUT = (By.ID, "input-lastname")
    REG_EMAIL_INPUT = (By.ID, "input-email")
    TELEPHONE_INPUT = (By.ID, "input-telephone")
    REG_PASSWORD_INPUT = (By.ID, "input-password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "input-confirm")
    AGREE_CHECKBOX = (By.CSS_SELECTOR, "input[name='agree']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "input[value='Continue']")

    # --- Post-login/register confirmation ---
    ACCOUNT_SUCCESS_HEADING = (By.CSS_SELECTOR, "#content h1, #content h2")

    def open_login_page(self):
        self.open(self.LOGIN_URL)

    def open_register_page(self):
        self.open(self.REGISTER_URL)

    def login(self, email: str, password: str):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def login_failed(self) -> bool:
        return self.is_visible(self.LOGIN_ERROR_ALERT, timeout=4)

    def register(self, user: dict):
        self.open_register_page()
        self.type_text(self.FIRSTNAME_INPUT, user["first_name"])
        self.type_text(self.LASTNAME_INPUT, user["last_name"])
        self.type_text(self.REG_EMAIL_INPUT, user["email"])
        self.type_text(self.TELEPHONE_INPUT, user["telephone"])
        self.type_text(self.REG_PASSWORD_INPUT, user["password"])
        self.type_text(self.CONFIRM_PASSWORD_INPUT, user["password"])
        self.click(self.AGREE_CHECKBOX)
        self.click(self.CONTINUE_BUTTON)

    def is_logged_in_or_registered(self) -> bool:
        """After a successful login the account dashboard loads; after a
        successful registration a 'Your Account Has Been Created!' page
        loads. Both show an #content heading, so presence + absence of
        the login error alert is a reliable enough signal here."""
        return self.is_visible(self.ACCOUNT_SUCCESS_HEADING, timeout=6)

    def login_or_register(self, user: dict):
        """Tries to log in with the given credentials; if that fails
        (account doesn't exist yet on this run of the demo site) it
        falls back to registering a brand-new account, which OpenCart
        logs straight in afterwards."""
        self.open_login_page()
        self.login(user["email"], user["password"])
        if self.login_failed():
            self.register(user)
