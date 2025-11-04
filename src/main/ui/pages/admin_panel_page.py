from playwright.sync_api import Page, expect
import allure
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.elements.user_bage_element import UserBadgeElement
from src.main.ui.pages.base_page import BasePage


class AdminPanelPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = self.page.locator("text='Admin Panel'")
        self.add_user_button = page.get_by_role("button", name="Add User")
        self.user_elements = self.page.locator('*:has-text("All Users")').locator('li')

    @property
    def url(self):
        return "/admin"

    def create_user(self, username, password, message: str = None):
        message =  message or "User created successfully!"
        with self.check_alert_message_and_accept(message):
            self.username_field.fill(username)
            self.password_field.fill(password)
            self.take_screenshot(username)

            self.add_user_button.click()

        return self

    def get_user(self):
        return self.get_page_elements(self.user_elements, UserBadgeElement)

    def find_user_by_username(self, username: str):
        user_locator = self.page.locator(f"li:has-text('{username}')").first
        try:
            expect(user_locator).to_have_text(username)
        except:
            pass

        user = [user for user in self.get_user() if user.username == username]
        return user[0] if user else None

    @allure.step("Get user from Dashboard")
    def find_user_by_request(self, request: CreateUserRequest):
        user_locator = self.page.locator(f"text={request.username}")
        user_locator.wait_for(state="attached")
        self.take_screenshot("user_list")
        user = user_locator.first
        assert user, "Could not find user in UI"
        return user

    def get_text_admin_panel(self) -> str:
        get_text = self.get_text(self.header)
        self.take_screenshot("get_text_admin_panel")
        return get_text

