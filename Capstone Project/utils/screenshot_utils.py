"""
Screenshot capture helper. Every screenshot is timestamped and named
after the step that triggered it, and the path is handed back so the
report generator can embed it.
"""

import os
import sys
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import config


def capture_screenshot(driver, step_name: str) -> str:
    safe_name = step_name.replace(" ", "_").lower()
    filename = f"{safe_name}_{int(time.time() * 1000)}.png"
    filepath = os.path.join(config.SCREENSHOTS_DIR, filename)
    driver.save_screenshot(filepath)
    return filepath
