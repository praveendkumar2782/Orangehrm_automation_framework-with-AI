# OrangeHRM Playwright Automation Framework

Production-grade UI test automation for [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login).

## Stack
- Python 3.13+
- Playwright (sync API)
- pytest + pytest-playwright
- Allure Reporting

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Run Tests
```bash
pytest
pytest --alluredir=allure-results
```

## Allure Reports
```bash
allure generate allure-results --clean -o reports/allure-report
allure serve allure-results
```

## Project Structure
```
Orangehrm_automation_framework/
├── config/settings.py      # URLs, credentials, timeouts
├── conftest.py             # page fixture, traces, failure screenshots
├── data/test_profiles.csv  # Externalized test data (5 profiles)
├── pages/playground_page.py
├── tests/test_suite.py
├── reports/allure-report/
└── allure-results/
```

## Features Covered
- Login, keyboard navigation, header/user dropdown
- PIM tables, autocomplete, dynamic dropdowns, add employee (CSV-driven)
- Leave List datepicker and dropdown filters
- Admin user management dropdowns and tables
- Directory search, Recruitment/Buzz file uploads
- My Info contact details (CSV-driven)
- Mouse hover, drag gestures, image verification
- Playwright trace on failure attached to Allure
