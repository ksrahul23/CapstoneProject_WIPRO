"""
Central configuration for the automation framework.
Keeping all environment-level values here means nothing else in the
project ever hardcodes a URL, timeout, or path.
"""

import os

BASE_URL = "https://tutorialsninja.com/demo/"

BROWSER = os.environ.get("BROWSER", "chrome")          # chrome | firefox
HEADLESS = os.environ.get("HEADLESS", "false").lower() == "true"

IMPLICIT_WAIT = 5          # seconds
EXPLICIT_WAIT = 15         # seconds

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")

JSON_TEST_DATA = os.path.join(DATA_DIR, "testdata.json")
EXCEL_TEST_DATA = os.path.join(DATA_DIR, "testdata.xlsx")   # optional

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
