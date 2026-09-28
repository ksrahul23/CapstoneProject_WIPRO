"""
Creates and configures the WebDriver instance.
Selenium 4's Selenium Manager resolves the matching driver binary
automatically, so no manual chromedriver/geckodriver download is needed.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import config


class DriverFactory:

    @staticmethod
    def get_driver(browser: str = None, headless: bool = None):
        browser = (browser or config.BROWSER).lower()
        headless = config.HEADLESS if headless is None else headless

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.implicitly_wait(config.IMPLICIT_WAIT)
        if browser == "chrome":
            driver.maximize_window()
        return driver
