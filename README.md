Autonomous AI-Driven Playwright & Pytest Automation Framework
A production-grade, enterprise-ready end-to-end test automation ecosystem built with Playwright, Pytest, and Allure reporting.

🚀 Engineered for the Future: This framework features an integrated AI-Agentic Execution Layer utilizing Model Context Protocol (MCP) and GitHub Copilot. It operates with autonomous data generation, zero test pollution, and a recursive self-healing debugging loop that ensures 100% stable builds before pushing to version control.

🤖 Core Innovation: The AI-Agentic Testing Lifecycle
Unlike traditional static automation suites, this framework is orchestrated via an autonomous AI agent layer using an MCP server and client context.

[Prompt/Intent] ──> [MCP Server] ──> [Dynamic CSV Generation] │ ┌─────────────────── [Self-Healing Loop] ◄──┤ │ ▼ ▼ [Pytest Execution] [Fix Script] ──> [Analyze Allure Results] │ ▲ ▼ └───── (If Fail) ── [Exit Code?] ── (If Pass 0 Errors) ──> [Auto Git Push]

1. Dynamic Data Seeding & Zero Test Pollution
The framework enforces a strict data isolation policy. Instead of relying on static mock data, the AI agent uses local filesystem MCP tools to dynamically generate highly distinct, randomized user profiles (name, email, phone, country) into data/test_profiles.csv prior to runtime. This eliminates data collisions and state contamination across parallel test runs.

2. Recursive Self-Healing Debugging Loop
The pipeline is wrapped in a conditional execution guardrail. If a test fails due to UI drift, a flaky locator, or an assertion mismatch:

The AI agent intercepts the Pytest exit code and parses raw Allure results and traceback logs.
It autonomously diagnoses the failure, accesses local system files via MCP tools, and rewrites the broken Playwright scripts.
The suite re-executes recursively until it achieves a zero-error, 100% pass rate gate.
3. Conditional DevOps Automation
The framework handles its own deployment criteria through smart prompting. The AI agent is restricted from pushing code blindly; it stages, commits, and pushes to GitHub only after a flawless execution verify step, generating and serving interactive Allure Reports automatically.





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
