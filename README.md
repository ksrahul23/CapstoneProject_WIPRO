# Capstone Project 1: Automate a Web Application Using Selenium WebDriver with Python

## Candidate Information

- **Student Name:** Rahul Kumar Shaw
- **Enrollment Number:** 12023002022132
- **Department:** CST (Computer Science and Technology)
- **Project Title:** Capstone Project 1 - Automate a Web Application Using Selenium WebDriver with Python

---

## Project Overview

This project provides an automated end-to-end test suite for an e-commerce platform (OpenCart demo: https://tutorialsninja.com/demo/) utilizing **Selenium WebDriver with Python**.

The project is structured according to the **Page Object Model (POM)** design pattern, ensuring modularity, code reusability, maintainability, and clean separation between test logic and UI locators.

---

## Key Features and Automated Flow

1. **Browser Initialization:**
   - Chrome / Firefox setup via Selenium 4 native driver management without manual binary installations.
   - Configurable headed or headless execution modes.

2. **User Authentication:**
   - Automated login functionality.
   - Automatic fallback registration for newly generated test users if an existing account is not present.

3. **Product Search:**
   - Search for specific products (e.g., MacBook) using the search bar and verify matching search results.

4. **Add to Cart:**
   - Add the selected product to the shopping cart and verify success notification alerts.

5. **Cart Quantity Management:**
   - Navigate to the shopping cart, modify item quantities, and trigger recalculations.

6. **Cart Verification:**
   - Validate that the cart accurately reflects product name, updated quantity, and line items.

7. **Alert and Modal Handling:**
   - Robust utilities to handle unexpected JavaScript popups, alerts, and Bootstrap modal overlays.

8. **Data-Driven Testing:**
   - External test data ingestion from JSON (`data/testdata.json`).
   - Built-in support for Excel (`data/testdata.xlsx`) via `openpyxl` with automatic fallback.

9. **Screenshot Capture & Reporting:**
   - Captures timestamped screenshots at every major test step and on test failure.
   - Generates a standalone HTML execution report (`reports/execution_report.html`) containing test summary cards, timestamps, pass/fail status, and embedded screenshots.

---

## Project Directory Structure

```
Capstone Project/
|-- main.py                     # Entry point to execute the complete test suite
|-- requirements.txt            # Python dependencies
|-- README.md                   # Project documentation and student information
|-- config/
|   |-- __init__.py
|   `-- config.py               # URLs, timeouts, browser settings, and directory paths
|-- data/
|   |-- testdata.json           # Test data (user credentials, product details, quantity)
|   `-- testdata.xlsx.md        # Instructions for optional Excel test data configuration
|-- pages/                      # Page Object Model classes
|   |-- __init__.py
|   |-- base_page.py            # Base page class with reusable explicit wait wrappers
|   |-- login_page.py           # Login and registration page actions and locators
|   |-- search_page.py          # Search bar and results listing actions and locators
|   `-- cart_page.py            # Shopping cart management and verification actions
|-- utils/                      # Helper utilities and framework components
|   |-- __init__.py
|   |-- driver_factory.py       # WebDriver factory supporting Chrome and Firefox
|   |-- data_reader.py          # Unified reader for JSON and Excel test data
|   |-- screenshot_utils.py     # Timestamped screenshot capture utility
|   |-- alert_handler.py        # JS alert and popup dismissal utilities
|   `-- report_generator.py     # Custom HTML execution report generator
|-- tests/                      # Test cases
|   |-- __init__.py
|   `-- test_ecommerce_flow.py  # Unittest end-to-end test implementation
`-- reports/
    |-- screenshots/            # Runtime directory storing test screenshots
    `-- execution_report.html   # Auto-generated execution report
```

---

## Installation and Setup

### 1. Prerequisites
- Python 3.8 or higher installed on your system.
- Google Chrome or Mozilla Firefox browser installed.

### 2. Create and Activate Virtual Environment

On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r "Capstone Project/requirements.txt"
```

---

## Running the Tests

### Option A: Run via Main Entry Script
```bash
cd "Capstone Project"
python main.py
```

### Option B: Run via Standard Unittest Runner
```bash
cd "Capstone Project"
python -m unittest tests/test_ecommerce_flow.py -v
```

### Headless Execution
To run tests in headless mode (ideal for CI/CD environments):
```cmd
set HEADLESS=true
python main.py
```

Or on Linux/macOS:
```bash
HEADLESS=true python main.py
```

---

## Viewing the Execution Report

After test execution, the standalone HTML report is saved at:
```
Capstone Project/reports/execution_report.html
```
Open this file in any web browser to view the step-by-step results, execution times, status badges, and captured screenshots.
