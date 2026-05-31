from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from config.settings import DATA_DIR, UPLOADS_DIR
from pages.playground_page import PlaygroundPage
from utils.data_loader import load_test_profiles


@pytest.fixture(scope="session")
def test_profiles() -> list[dict]:
    return load_test_profiles()


@pytest.fixture(scope="session", autouse=True)
def create_upload_fixtures():
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "resume_emma.pdf": b"%PDF-1.4 Emma Wilson Resume",
        "resume_liam.pdf": b"%PDF-1.4 Liam Chen Resume",
        "photo_sophia.png": (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
            b"\x00\x00\x00\x0aIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
            b"\x0d\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        ),
        "photo_noah.png": (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
            b"\x00\x00\x00\x0aIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
            b"\x0d\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        ),
    }
    for filename, content in files.items():
        path = UPLOADS_DIR / filename
        if not path.exists():
            path.write_bytes(content)


@pytest.fixture
def app(page: Page) -> PlaygroundPage:
    return PlaygroundPage(page)


@allure.feature("Authentication")
@allure.story("Login Page Interactions")
class TestLogin:
    def test_login_page_fields_and_branding(self, app: PlaygroundPage):
        app.navigate_to_login()
        app.verify_login_page_loaded()
        app.verify_login_logo_visible()
        app.verify_login_footer_visible()

    def test_login_with_valid_credentials(self, app: PlaygroundPage):
        app.login()
        app.verify_dashboard_loaded()

    def test_login_form_field_interactions(self, app: PlaygroundPage, test_profiles: list[dict]):
        profile = test_profiles[0]
        app.navigate_to_login()
        app.fill_username(profile["email"].split("@")[0])
        app.fill_password("wrong-password")
        app.clear_login_form()
        app.fill_username("Admin")
        app.fill_password("admin123")
        app.submit_login()
        app.verify_dashboard_loaded()


@allure.feature("Authentication")
@allure.story("Keyboard Navigation")
class TestKeyboardActions:
    def test_tab_through_login_fields(self, app: PlaygroundPage):
        app.navigate_to_login()
        app.tab_through_login_fields()

    def test_login_using_keyboard_submit(self, app: PlaygroundPage):
        app.navigate_to_login()
        app.navigate_login_with_keyboard("Admin", "admin123")
        app.verify_dashboard_loaded()


@allure.feature("Header and Footer")
@allure.story("Global Navigation")
class TestHeaderFooter:
    def test_header_and_user_dropdown(self, app: PlaygroundPage):
        app.login()
        app.verify_header_visible()
        app.verify_user_dropdown_options(["About", "Support", "Change Password", "Logout"])

    def test_logout_returns_to_login(self, app: PlaygroundPage):
        app.login()
        app.logout()


@allure.feature("PIM Module")
@allure.story("Tables and Dynamic Dropdowns")
class TestPimModule:
    def test_employee_list_table(self, app: PlaygroundPage):
        app.login()
        app.go_to_pim_employee_list()
        app.verify_table_has_minimum_rows(1)

    def test_autocomplete_employee_search(self, app: PlaygroundPage):
        app.login()
        app.go_to_pim_employee_list()
        app.search_autocomplete("Peter")
        app.verify_autocomplete_suggestion_visible("Peter")

    def test_job_title_dropdown_filter(self, app: PlaygroundPage):
        app.login()
        app.go_to_pim_employee_list()
        selected_value = app.select_first_available_dropdown_option(2)
        app.verify_dropdown_value(2, selected_value)

    @pytest.mark.parametrize("profile", load_test_profiles()[:1], ids=lambda p: p["name"])
    def test_add_employee_from_csv(self, app: PlaygroundPage, profile: dict):
        app.login()
        app.go_to_pim_employee_list()
        app.open_add_employee_form()
        app.add_employee_from_profile(profile)


@allure.feature("Leave Module")
@allure.story("Datepicker Interactions")
class TestLeaveModule:
    def test_leave_list_datepicker(self, app: PlaygroundPage):
        app.login()
        app.go_to_leave_list()
        app.open_datepicker(0)
        app.verify_calendar_visible()
        app.select_calendar_day("15")
        expect(app.page.locator(".oxd-date-input input").first).not_to_have_value("")

    def test_leave_list_dropdown_filter(self, app: PlaygroundPage):
        app.login()
        app.go_to_leave_list()
        selected_value = app.select_first_available_dropdown_option(0)
        app.verify_dropdown_value(0, selected_value)
        expect(app.page.get_by_role("heading", name="Leave List")).to_be_visible()


@allure.feature("Admin Module")
@allure.story("Standard Dropdowns and Tables")
class TestAdminModule:
    def test_system_users_table(self, app: PlaygroundPage):
        app.login()
        app.go_to_admin_users()
        app.verify_table_has_minimum_rows(1)

    def test_add_user_form_dropdowns(self, app: PlaygroundPage):
        app.login()
        app.go_to_admin_users()
        app.open_add_system_user_form()
        app.select_from_dropdown(0, "Admin")
        app.verify_dropdown_value(0, "Admin")
        app.select_from_dropdown(1, "Enabled")
        app.verify_dropdown_value(1, "Enabled")


@allure.feature("Directory Module")
@allure.story("Search and Cards")
class TestDirectoryModule:
    def test_directory_search(self, app: PlaygroundPage, test_profiles: list[dict]):
        app.login()
        app.go_to_directory()
        app.search_directory("Peter Mac Anderson")
        expect(app.page.locator(".orangehrm-directory-card, .oxd-table-body .oxd-table-row").first).to_be_visible()


@allure.feature("Recruitment Module")
@allure.story("File Upload")
class TestFileUpload:
    def test_single_file_upload_candidate_resume(self, app: PlaygroundPage, test_profiles: list[dict]):
        app.login()
        app.go_to_add_candidate()
        app.fill_candidate_form(test_profiles[0])
        resume_path = UPLOADS_DIR / "resume_emma.pdf"
        app.upload_single_file(resume_path)
        expect(app.page.locator('input[type="file"]')).to_be_attached()

    def test_multiple_file_upload_sequential(self, app: PlaygroundPage, test_profiles: list[dict]):
        app.login()
        app.go_to_add_candidate()
        app.fill_candidate_form(test_profiles[1])
        files = [
            UPLOADS_DIR / "resume_emma.pdf",
            UPLOADS_DIR / "resume_liam.pdf",
        ]
        app.upload_multiple_files(files)
        expect(app.page.locator('input[type="file"]')).to_be_attached()


@allure.feature("Buzz Module")
@allure.story("Social Feed and Photo Upload")
class TestBuzzModule:
    def test_post_buzz_message(self, app: PlaygroundPage, test_profiles: list[dict]):
        app.login()
        app.go_to_buzz()
        message = f"Automated post from {test_profiles[2]['name']}"
        app.post_buzz_message(message)
        expect(app.page.locator(".oxd-buzz-post-input")).to_have_value("")

    def test_buzz_photo_upload(self, app: PlaygroundPage):
        app.login()
        app.go_to_buzz()
        app.share_buzz_photo(UPLOADS_DIR / "photo_sophia.png")
        expect(app.page.locator('input[type="file"]')).to_be_attached()


@allure.feature("My Info Module")
@allure.story("Contact Details Form")
class TestMyInfoModule:
    def test_update_contact_details_from_csv(self, app: PlaygroundPage, test_profiles: list[dict]):
        app.login()
        app.go_to_my_info_contact_details()
        app.update_contact_details(test_profiles[3])

    def test_profile_image_section_visible(self, app: PlaygroundPage):
        app.login()
        app.open_sidebar_menu("My Info")
        app.verify_profile_image_section()


@allure.feature("Mouse Actions")
@allure.story("Hover and Drag Gestures")
class TestMouseActions:
    def test_sidebar_menu_hover(self, app: PlaygroundPage):
        app.login()
        app.hover_sidebar_menu("PIM")
        expect(app.page.get_by_role("link", name="PIM", exact=True)).to_be_visible()

    def test_drag_and_drop_sidebar_gesture(self, app: PlaygroundPage):
        app.login()
        app.perform_drag_and_drop_gesture("Admin", "PIM")
        expect(app.page.locator(".oxd-sidepanel")).to_be_visible()


@allure.feature("Image Verification")
@allure.story("Visual Element Checks")
class TestImageVerification:
    def test_login_logo_image_verification(self, app: PlaygroundPage):
        app.navigate_to_login()
        app.verify_image_element_visible(app.login_logo, name="login_logo")

    def test_dashboard_header_image_elements(self, app: PlaygroundPage):
        app.login()
        app.verify_header_visible()
        app.verify_image_element_visible(app.user_dropdown_tab, name="user_avatar")
