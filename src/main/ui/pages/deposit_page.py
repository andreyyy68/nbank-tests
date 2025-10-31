from src.main.ui.pages.base_page import BasePage
from playwright.sync_api import Page
import re


class DepositPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.deposit_button = self.page.get_by_role("button", name="Deposit")

    @property
    def url(self):
        return "/deposit"

    def select_account(self, account_id: int):
        self.choose_an_account.select_option(value=str(account_id))
        return self

    def enter_amount(self, amount: int | float):
        self.fill_amount.fill(str(amount))
        return self

    def submit_deposit(self, message: str):
        with self.check_alert_message_and_accept(message):
            self.deposit_button.click(force=True)
        return self

    def submit_deposit_expecting_error(self, message):
        self._handle_alert_before_click(message=message, button_locator=self.deposit_button)
        return self

    def parse_deposit_alert(self):
        match = re.search(r"Successfully deposited \$([\d.]+)", self.current_alert_message)
        if match:
            self.deposit_amount = float(match.group(1))
        return self.deposit_amount