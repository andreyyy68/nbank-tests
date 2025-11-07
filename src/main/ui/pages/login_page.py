from src.main.ui.pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_button = page.get_by_role('button', name='Login')

    @property
    def url(self):
        return "/login"

    def login(self, username: str, password: str):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.take_screenshot("fill_username_and_password")
        self.login_button.click()
        return self