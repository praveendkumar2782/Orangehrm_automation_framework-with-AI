import os
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config.settings import DEFAULT_TIMEOUT, TRACES_DIR, VIEWPORT


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
    }


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": VIEWPORT,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args, request) -> BrowserContext:
    trace_mode = request.config.getoption("--tracing", default="retain-on-failure")
    traces_dir = TRACES_DIR
    traces_dir.mkdir(parents=True, exist_ok=True)

    context = browser.new_context(**browser_context_args)
    context.set_default_timeout(DEFAULT_TIMEOUT)

    if trace_mode in {"on", "retain-on-failure", "on-first-retry"}:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    trace_path = traces_dir / f"{request.node.name}.zip"
    if trace_mode == "on":
        context.tracing.stop(path=str(trace_path))
        _attach_trace_to_allure(trace_path, request)
    elif trace_mode == "retain-on-failure":
        rep = getattr(request.node, "rep_call", None)
        if rep is not None and rep.failed:
            context.tracing.stop(path=str(trace_path))
            _attach_trace_to_allure(trace_path, request)
        else:
            context.tracing.stop()
    elif trace_mode == "on-first-retry":
        rep = getattr(request.node, "rep_call", None)
        if rep is not None and rep.failed and hasattr(request.node, "execution_count"):
            if request.node.execution_count > 1:
                context.tracing.stop(path=str(trace_path))
                _attach_trace_to_allure(trace_path, request)
            else:
                context.tracing.stop()
        else:
            context.tracing.stop()
    else:
        context.tracing.stop()

    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when != "call" or rep.failed is False:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    try:
        screenshot = page.screenshot(full_page=True, timeout=5000)
        allure.attach(
            screenshot,
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:
        allure.attach(
            str(exc),
            name="failure_screenshot_error",
            attachment_type=allure.attachment_type.TEXT,
        )


def _attach_trace_to_allure(trace_path: Path, request) -> None:
    if not trace_path.exists():
        return

    with open(trace_path, "rb") as trace_file:
        allure.attach(
            trace_file.read(),
            name=f"playwright_trace_{request.node.name}",
            attachment_type=allure.attachment_type.ZIP,
            extension="zip",
        )

    allure.attach(
        f"Playwright trace saved to: {trace_path.resolve()}\n"
        f"View with: playwright show-trace {trace_path.resolve()}",
        name="trace_view_instructions",
        attachment_type=allure.attachment_type.TEXT,
    )


@pytest.fixture(scope="session", autouse=True)
def ensure_directories():
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path("allure-results").mkdir(exist_ok=True)
