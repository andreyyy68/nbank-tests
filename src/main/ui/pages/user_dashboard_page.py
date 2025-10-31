from playwright.async_api import Page
from src.main.ui.pages.base_page import BasePage
from src.main.ui.constants.alert_message import AlertMessage
import re


class UserDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = page.locator("text='User Dashboard'")
        self.welcome_text = page.locator(".welcome-text")
        self.create_account_button = page.get_by_role("button", name="Create New Account")
        self.deposit_money_button = page.get_by_role("button", name="Deposit Money")

    @property
    def url(self):
        return "/dashboard"

    def create_account(self):
        with self.check_alert_message_and_accept(AlertMessage.ACCOUNT_CREATED):
            self.create_account_button.click()
        return self

    def create_account_and_get_account_number(self):
        self.create_account()
        account_number = None
        match = re.search(r"Account Number: (\w+)", self.current_alert_message)
        if match:
            account_number = match.group(1)
        assert account_number, "Could not extract account number"
        return account_number

    def get_text_user_dashboard(self) -> str:
        return self.get_text(self.header)
