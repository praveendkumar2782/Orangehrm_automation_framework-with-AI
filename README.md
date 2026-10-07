[2_project_README.md](https://github.com/user-attachments/files/33150598/2_project_README.md)<!-- Replace the README.md of Orangehrm_automation_framework-with-AI with this.
     Items marked [CONFIRM] are claims only YOU can verify. Keep a line only if it is true
     and you can demo it in an interview. Delete the rest. -->

# OrangeHRM Playwright Automation Framework (Python)

UI test automation for the [OrangeHRM demo site](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login),
built with Playwright, pytest and Allure. Test code was authored with AI assistance (Cursor + MCP) and reviewed by me.

![Allure report screenshot](docs/allure-report.png) <!-- add a screenshot -->

## Tech stack
- Python 3.13+, Playwright (sync API)
- pytest + pytest-playwright
- Allure reporting (Playwright trace and screenshot attached on failure)
- GitHub Actions (CI)

## Design
- **Page Object Model:** locators and actions live in `pages/`, tests stay readable
- **Fixtures:** browser/page setup, traces and failure screenshots in `conftest.py`
- **Externalised data:** test profiles in `data/test_profiles.csv`
- **Central config:** URLs and timeouts in `config/settings.py`

## What's covered
- Login, keyboard navigation, header/user dropdown
- PIM: tables, autocomplete, dynamic dropdowns, add employee (CSV-driven)
- Leave List: datepicker and dropdown filters
- Admin: user management dropdowns and tables
- Directory search, Recruitment/Buzz file uploads
- My Info contact details (CSV-driven)
- Mouse hover, drag gestures, image verification

## How AI was used
- Cursor with MCP (filesystem tools) to generate test cases and the randomised CSV test data
- AI-assisted debugging of failing tests from Allure results and tracebacks
- [CONFIRM] Include only if true: "Fixes suggested by the AI were reviewed and committed manually"
- [CONFIRM] Include only if you have the files in the repo: link to your MCP config / prompt / agent rules here

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Run tests
```bash
pytest
pytest --alluredir=allure-results
```

## Allure report
```bash
allure generate allure-results --clean -o reports/allure-report
allure serve allure-results
```

## Project structure
```
├── config/settings.py
├── conftest.py
├── data/test_profiles.csv
├── pages/
├── tests/
├── utils/
├── pytest.ini
└── requirements.txt
```

## CI
Tests run on every push via GitHub Actions (`.github/workflows/tests.yml`).
The demo site is public and can be slow or reset, so occasional failures may come from the site, not the tests.

## Roadmap
- Salesforce Lightning suite (separate repo)
- TypeScript version of the framework
- Parallel execution with pytest-xdist
