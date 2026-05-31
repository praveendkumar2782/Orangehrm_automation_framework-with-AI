import re
from pathlib import Path

import allure
from playwright.sync_api import Locator, Page, expect

from config.settings import (
    DASHBOARD_URL,
    DEFAULT_PASSWORD,
    DEFAULT_TIMEOUT,
    DEFAULT_USERNAME,
    LOGIN_URL,
)


class PlaygroundPage:
    """Page Object Model for OrangeHRM demo application."""

    def __init__(self, page: Page) -> None:
        self.page = page

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #

    @allure.step("Navigate to login page")
    def navigate_to_login(self) -> None:
        last_error = None
        for _ in range(3):
            try:
                self.page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
                self.page.wait_for_load_state("networkidle")
                return
            except Exception as exc:
                last_error = exc
        raise last_error

    @allure.step("Navigate to dashboard")
    def navigate_to_dashboard(self) -> None:
        self.page.goto(DASHBOARD_URL, wait_until="networkidle")

    @allure.step("Open sidebar menu: {menu_name}")
    def open_sidebar_menu(self, menu_name: str) -> None:
        self.page.get_by_role("link", name=menu_name, exact=True).click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Open submenu: {submenu_name}")
    def open_submenu(self, submenu_name: str) -> None:
        self.page.get_by_role("link", name=submenu_name, exact=True).click()
        self.page.wait_for_load_state("networkidle")

    # ------------------------------------------------------------------ #
    # Login page
    # ------------------------------------------------------------------ #

    @property
    def username_input(self) -> Locator:
        return self.page.get_by_placeholder("Username")

    @property
    def password_input(self) -> Locator:
        return self.page.get_by_placeholder("Password")

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role("button", name="Login")

    @property
    def login_logo(self) -> Locator:
        return self.page.locator(".orangehrm-login-branding img")

    @property
    def login_footer(self) -> Locator:
        return self.page.locator(".orangehrm-login-footer-sm, .orangehrm-login-footer")

    @allure.step("Fill username: {username}")
    def fill_username(self, username: str) -> None:
        self.username_input.click()
        self.username_input.fill(username)

    @allure.step("Fill password")
    def fill_password(self, password: str) -> None:
        self.password_input.click()
        self.password_input.fill(password)

    @allure.step("Clear login form fields")
    def clear_login_form(self) -> None:
        self.username_input.clear()
        self.password_input.clear()

    @allure.step("Submit login form")
    def submit_login(self) -> None:
        self.login_button.click()
        self.page.wait_for_url(re.compile(r".*/dashboard/index$"), timeout=DEFAULT_TIMEOUT)

    @allure.step("Login with username={username}")
    def login(self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD) -> None:
        self.navigate_to_login()
        self.fill_username(username)
        self.fill_password(password)
        self.submit_login()

    @allure.step("Verify login page is displayed")
    def verify_login_page_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/auth/login$"))
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()

    @allure.step("Verify login branding image")
    def verify_login_logo_visible(self) -> None:
        expect(self.login_logo).to_be_visible()
        expect(self.login_logo).to_have_attribute("src", re.compile(r".*ohrm_branding.*"))

    @allure.step("Verify login footer is visible")
    def verify_login_footer_visible(self) -> None:
        expect(self.login_footer.first).to_be_visible()

    @allure.step("Verify dashboard after successful login")
    def verify_dashboard_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/dashboard/index$"))
        expect(self.page.locator(".oxd-topbar")).to_be_visible()
        expect(self.page.locator(".oxd-sidepanel")).to_be_visible()

    # ------------------------------------------------------------------ #
    # Header / user dropdown (bootstrap-style menu)
    # ------------------------------------------------------------------ #

    @property
    def header(self) -> Locator:
        return self.page.locator(".oxd-topbar")

    @property
    def user_dropdown_tab(self) -> Locator:
        return self.page.locator(".oxd-userdropdown-tab")

    @allure.step("Open user profile dropdown")
    def open_user_dropdown(self) -> None:
        self.user_dropdown_tab.click()

    @allure.step("Select user dropdown option: {option}")
    def select_user_dropdown_option(self, option: str) -> None:
        self.open_user_dropdown()
        self.page.get_by_role("menuitem", name=option).click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Verify header is visible")
    def verify_header_visible(self) -> None:
        expect(self.header).to_be_visible()
        expect(self.user_dropdown_tab).to_be_visible()

    @allure.step("Verify user dropdown options")
    def verify_user_dropdown_options(self, expected_options: list[str]) -> None:
        self.open_user_dropdown()
        for option in expected_options:
            expect(self.page.get_by_role("menuitem", name=option)).to_be_visible()
        self.page.keyboard.press("Escape")

    @allure.step("Logout from application")
    def logout(self) -> None:
        self.select_user_dropdown_option("Logout")
        self.verify_login_page_loaded()

    # ------------------------------------------------------------------ #
    # Standard & dynamic dropdowns
    # ------------------------------------------------------------------ #

    @allure.step("Open dropdown at index {index}")
    def open_dropdown_by_index(self, index: int = 0) -> None:
        dropdown = self.page.locator(".oxd-select-wrapper").nth(index)
        expect(dropdown).to_be_visible()
        dropdown.click()
        expect(self.page.locator(".oxd-select-dropdown")).to_be_visible(timeout=DEFAULT_TIMEOUT)

    @allure.step("Select dropdown option: {option_text}")
    def select_dropdown_option(self, option_text: str) -> None:
        option = self.page.get_by_role("option", name=option_text)
        expect(option).to_be_visible()
        option.click()

    @allure.step("Select dropdown option by index {dropdown_index}: {option_text}")
    def select_from_dropdown(self, dropdown_index: int, option_text: str) -> None:
        self.open_dropdown_by_index(dropdown_index)
        self.select_dropdown_option(option_text)

    @allure.step("Select first available option from dropdown index {dropdown_index}")
    def select_first_available_dropdown_option(self, dropdown_index: int) -> str:
        self.open_dropdown_by_index(dropdown_index)
        option = self.page.get_by_role("option").filter(has_not_text="-- Select --").first
        expect(option).to_be_visible()
        option_text = option.inner_text()
        option.click()
        return option_text

    @allure.step("Verify dropdown shows value: {expected_value}")
    def verify_dropdown_value(self, dropdown_index: int, expected_value: str) -> None:
        dropdown_text = self.page.locator(".oxd-select-wrapper").nth(dropdown_index).locator(
            ".oxd-select-text"
        )
        expect(dropdown_text).to_have_text(expected_value)

    # ------------------------------------------------------------------ #
    # Autocomplete / dynamic dropdown (wiki-style search hints)
    # ------------------------------------------------------------------ #

    @allure.step("Search autocomplete field with query: {query}")
    def search_autocomplete(self, query: str, field_index: int = 0) -> None:
        field = self.page.get_by_placeholder("Type for hints...").nth(field_index)
        field.click()
        field.fill(query)
        self.page.wait_for_timeout(1500)

    @allure.step("Select autocomplete option containing: {text}")
    def select_autocomplete_option(self, text: str) -> None:
        option = self.page.locator(".oxd-autocomplete-option").filter(has_text=text)
        expect(option.first).to_be_visible()
        option.first.click()

    @allure.step("Verify autocomplete suggestions contain: {text}")
    def verify_autocomplete_suggestion_visible(self, text: str) -> None:
        expect(self.page.locator(".oxd-autocomplete-option").filter(has_text=text).first).to_be_visible()

    # ------------------------------------------------------------------ #
    # Datepicker / dynamic calendar
    # ------------------------------------------------------------------ #

    @allure.step("Open datepicker at index {index}")
    def open_datepicker(self, index: int = 0) -> None:
        self.page.locator(".oxd-date-input .oxd-icon").nth(index).click()

    @allure.step("Select calendar day: {day}")
    def select_calendar_day(self, day: str) -> None:
        calendar_day = self.page.locator(".oxd-calendar-date").filter(has_text=re.compile(rf"^{day}$"))
        expect(calendar_day.first).to_be_visible()
        calendar_day.first.click()

    @allure.step("Navigate calendar to next month")
    def go_to_next_calendar_month(self) -> None:
        self.page.locator(".oxd-calendar-selector-month-selected ~ .oxd-icon").first.click()

    @allure.step("Fill datepicker at index {index} with day {day}")
    def pick_date(self, index: int, day: str) -> None:
        self.open_datepicker(index)
        self.select_calendar_day(day)

    @allure.step("Verify calendar is visible")
    def verify_calendar_visible(self) -> None:
        expect(self.page.locator(".oxd-calendar-date").first).to_be_visible()

    # ------------------------------------------------------------------ #
    # Tables
    # ------------------------------------------------------------------ #

    @property
    def table_body_rows(self) -> Locator:
        return self.page.locator(".oxd-table-body .oxd-table-row")

    @allure.step("Verify table has at least {min_rows} rows")
    def verify_table_has_minimum_rows(self, min_rows: int = 1) -> None:
        expect(self.table_body_rows.first).to_be_visible()
        row_count = self.table_body_rows.count()
        assert row_count >= min_rows, f"Expected at least {min_rows} rows, found {row_count}"

    @allure.step("Verify table contains text: {text}")
    def verify_table_contains_text(self, text: str) -> None:
        expect(self.page.locator(".oxd-table-body")).to_contain_text(text)

    @allure.step("Click first table row")
    def click_first_table_row(self) -> None:
        self.table_body_rows.first.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Get dynamic table row count")
    def get_table_row_count(self) -> int:
        return self.table_body_rows.count()

    # ------------------------------------------------------------------ #
    # Forms & text fields
    # ------------------------------------------------------------------ #

    @allure.step("Fill input by name: {field_name}")
    def fill_input_by_name(self, field_name: str, value: str) -> None:
        self.page.locator(f'input[name="{field_name}"]').fill(value)

    @allure.step("Fill input by placeholder: {placeholder}")
    def fill_input_by_placeholder(self, placeholder: str, value: str) -> None:
        self.page.get_by_placeholder(placeholder).fill(value)

    @allure.step("Fill input by label: {label}")
    def fill_input_by_label(self, label: str, value: str) -> None:
        group = self.page.locator(".oxd-input-group").filter(
            has=self.page.locator("label").filter(has_text=re.compile(rf"^{re.escape(label)}"))
        )
        group.locator("input").fill(value)

    @allure.step("Fill textarea")
    def fill_textarea(self, value: str, index: int = 0) -> None:
        self.page.locator("textarea").nth(index).fill(value)

    @allure.step("Toggle switch at index {index}")
    def toggle_switch(self, index: int = 0) -> None:
        self.page.locator(".oxd-switch-input").nth(index).click()

    @allure.step("Click button: {name}")
    def click_button(self, name: str) -> None:
        self.page.get_by_role("button", name=name).click()
        self.page.wait_for_load_state("networkidle")

    # ------------------------------------------------------------------ #
    # PIM module
    # ------------------------------------------------------------------ #

    @allure.step("Navigate to PIM employee list")
    def go_to_pim_employee_list(self) -> None:
        self.open_sidebar_menu("PIM")

    @allure.step("Open add employee form")
    def open_add_employee_form(self) -> None:
        self.click_button("Add")

    @allure.step("Add employee from profile data")
    def add_employee_from_profile(self, profile: dict) -> None:
        first_name, *last_parts = profile["name"].split(" ", 1)
        last_name = last_parts[0] if last_parts else "User"
        self.fill_input_by_name("firstName", first_name)
        self.fill_input_by_name("middleName", "")
        self.fill_input_by_name("lastName", last_name)
        self.click_button("Save")
        expect(self.page.get_by_text("Successfully Saved")).to_be_visible(timeout=DEFAULT_TIMEOUT)

    @allure.step("Filter employees by job title: {job_title}")
    def filter_by_job_title(self, job_title: str) -> None:
        self.select_from_dropdown(2, job_title)
        self.click_button("Search")

    # ------------------------------------------------------------------ #
    # Leave module
    # ------------------------------------------------------------------ #

    @allure.step("Navigate to Leave List")
    def go_to_leave_list(self) -> None:
        self.open_sidebar_menu("Leave")
        self.open_submenu("Leave List")

    @allure.step("Navigate to Leave Apply form")
    def go_to_leave_apply(self) -> None:
        self.open_sidebar_menu("Leave")
        self.open_submenu("Apply")

    @allure.step("Filter leave list by status: {status}")
    def filter_leave_list(self, status: str) -> None:
        self.select_from_dropdown(0, status)
        self.click_button("Search")

    # ------------------------------------------------------------------ #
    # Admin module
    # ------------------------------------------------------------------ #

    @allure.step("Navigate to Admin System Users")
    def go_to_admin_users(self) -> None:
        self.open_sidebar_menu("Admin")

    @allure.step("Open add system user form")
    def open_add_system_user_form(self) -> None:
        self.click_button("Add")

    # ------------------------------------------------------------------ #
    # Directory module
    # ------------------------------------------------------------------ #

    @allure.step("Navigate to Directory")
    def go_to_directory(self) -> None:
        self.open_sidebar_menu("Directory")

    @allure.step("Search directory with employee name: {name}")
    def search_directory(self, name: str) -> None:
        query = name.split()[0]
        self.search_autocomplete(query, field_index=0)
        self.select_autocomplete_option(name.split()[0])
        self.click_button("Search")

    @allure.step("Verify directory cards are visible")
    def verify_directory_cards_visible(self) -> None:
        expect(self.page.locator(".orangehrm-directory-card").first).to_be_visible()

    # ------------------------------------------------------------------ #
    # Recruitment / file uploads
    # ------------------------------------------------------------------ #

    @allure.step("Navigate to Recruitment Add Candidate")
    def go_to_add_candidate(self) -> None:
        self.open_sidebar_menu("Recruitment")
        self.open_submenu("Candidates")
        self.click_button("Add")

    @allure.step("Upload single file: {file_path}")
    def upload_single_file(self, file_path: Path) -> None:
        file_input = self.page.locator('input[type="file"]')
        expect(file_input).to_be_attached()
        file_input.set_input_files(str(file_path))

    @allure.step("Upload multiple files sequentially")
    def upload_multiple_files(self, file_paths: list[Path]) -> None:
        file_input = self.page.locator('input[type="file"]')
        for file_path in file_paths:
            file_input.set_input_files(str(file_path))
            expect(file_input).to_be_attached()

    @allure.step("Fill candidate form from profile")
    def fill_candidate_form(self, profile: dict) -> None:
        first_name, *last_parts = profile["name"].split(" ", 1)
        last_name = last_parts[0] if last_parts else "Candidate"
        self.fill_input_by_name("firstName", first_name)
        self.fill_input_by_name("lastName", last_name)
        self.fill_input_by_label("Email", profile["email"])

    # ------------------------------------------------------------------ #
    # Buzz module
    # ------------------------------------------------------------------ #

    @allure.step("Navigate to Buzz feed")
    def go_to_buzz(self) -> None:
        self.open_sidebar_menu("Buzz")

    @allure.step("Post buzz message: {message}")
    def post_buzz_message(self, message: str) -> None:
        self.page.locator(".oxd-buzz-post-input").fill(message)
        self.page.get_by_role("button", name="Post", exact=True).click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Share photo on Buzz")
    def share_buzz_photo(self, file_path: Path) -> None:
        self.page.get_by_text("Share Photos").click()
        self.upload_single_file(file_path)

    # ------------------------------------------------------------------ #
    # My Info / Contact Details
    # ------------------------------------------------------------------ #

    @allure.step("Navigate to My Info Contact Details")
    def go_to_my_info_contact_details(self) -> None:
        self.open_sidebar_menu("My Info")
        self.open_submenu("Contact Details")

    @allure.step("Update contact details from profile")
    def update_contact_details(self, profile: dict) -> None:
        self.fill_input_by_label("Street 1", profile["address"])
        self.fill_input_by_label("Mobile", profile["phone"])
        self.fill_input_by_label("Work Email", profile["email"])
        self.click_button("Save")
        expect(self.page.get_by_text("Successfully Updated")).to_be_visible(timeout=DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------ #
    # Mouse & keyboard actions
    # ------------------------------------------------------------------ #

    @allure.step("Hover over sidebar menu: {menu_name}")
    def hover_sidebar_menu(self, menu_name: str) -> None:
        menu_item = self.page.get_by_role("link", name=menu_name, exact=True)
        menu_item.hover()

    @allure.step("Perform drag gesture from {source_menu} area to {target_menu} area")
    def perform_drag_and_drop_gesture(self, source_menu: str, target_menu: str) -> None:
        source = self.page.get_by_role("link", name=source_menu, exact=True)
        target = self.page.get_by_role("link", name=target_menu, exact=True)
        source.drag_to(target)

    @allure.step("Navigate login form using keyboard")
    def navigate_login_with_keyboard(self, username: str, password: str) -> None:
        self.username_input.click()
        self.username_input.fill(username)
        self.page.keyboard.press("Tab")
        self.password_input.fill(password)
        self.page.keyboard.press("Enter")
        self.page.wait_for_url(re.compile(r".*/dashboard/index$"), timeout=DEFAULT_TIMEOUT)

    @allure.step("Tab through login fields")
    def tab_through_login_fields(self) -> None:
        self.username_input.click()
        self.page.keyboard.press("Tab")
        expect(self.password_input).to_be_focused()
        self.page.keyboard.press("Tab")
        expect(self.login_button).to_be_focused()

    # ------------------------------------------------------------------ #
    # Image verification
    # ------------------------------------------------------------------ #

    @allure.step("Verify element image matches snapshot: {name}")
    def verify_image_element_visible(self, locator: Locator, name: str = "image") -> None:
        expect(locator).to_be_visible()
        allure.attach(
            locator.screenshot(),
            name=f"{name}_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    @allure.step("Verify profile image section on My Info")
    def verify_profile_image_section(self) -> None:
        expect(self.page.get_by_role("img", name="profile picture").first).to_be_visible()
