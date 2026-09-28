"""
Entry point: run `python main.py` to execute the full automation suite
and generate the HTML execution report.
"""

import sys
import unittest


def run():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName("tests.test_ecommerce_flow")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run()
