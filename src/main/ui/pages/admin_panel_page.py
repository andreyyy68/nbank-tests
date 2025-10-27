from playwright.sync_api import Page, expect
from src.main.api.models.comparison.model_assertions import ModelAssertions
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
            self.add_user_button.click()
        return self

    def get_user(self):
        return self.get_page_elements(self.user_elements, UserBadgeElement)

    def find_user_by_username(self, username: str):
        user_locator = self.page.locator(f"li:has-text('{username}')").first
        try:
            expect(user_locator).to_be_visible()
        except:
            pass

        user = [user for user in self.get_user() if user.username == username]
        return user[0] if user else None

    def find_user_by_request(self, request: CreateUserRequest):
        user = self.find_user_by_username(request.username)
        assert user, "Could not find user in UI"
        ModelAssertions(user, request).match()
