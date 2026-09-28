"""
Handles native JS alerts/confirms/prompts and in-page modal popups
(e.g. OpenCart's "Success: You have added ..." Bootstrap alert banner)
so a stray dialog never blocks the run.
"""

from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


def handle_js_alert_if_present(driver, timeout: int = 3, accept: bool = True) -> bool:
    """Accepts (or dismisses) a native JavaScript alert if one appears."""
    try:
        WebDriverWait(driver, timeout).until(lambda d: _alert_present(d))
        alert = driver.switch_to.alert
        text = alert.text
        if accept:
            alert.accept()
        else:
            alert.dismiss()
        return True
    except (TimeoutException, NoAlertPresentException):
        return False


def _alert_present(driver) -> bool:
    try:
        driver.switch_to.alert
        return True
    except NoAlertPresentException:
        return False


def dismiss_inpage_popup_if_present(driver, close_selector: str, timeout: int = 3) -> bool:
    """Closes a Bootstrap-style in-page popup/banner (e.g. a newsletter
    modal or a cookie-consent banner) identified by a CSS close-button
    selector, if it's present on the page."""
    from selenium.webdriver.common.by import By

    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, close_selector)
        )
        driver.find_element(By.CSS_SELECTOR, close_selector).click()
        return True
    except TimeoutException:
        return False
