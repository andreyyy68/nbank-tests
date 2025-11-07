from src.main.ui.pages.base_page import BasePage
import re
from playwright.sync_api import expect



class TransferPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.recipient_name = self.page.get_by_placeholder("Enter recipient name")
        self.recipient_account_number = self.page.get_by_placeholder("Enter recipient account number")
        self.transfer_button = self.page.get_by_role("button", name="Send Transfer")
        self.transfer_again_button = self.page.get_by_role("button", name="Transfer Again")
        self.to_find_transaction_name = self.page.get_by_placeholder("Enter name to find transactions")
        self.button_search_transaction = self.page.get_by_role("button", name="Search Transactions")


    @property
    def url(self):
        return "/transfer"

    def select_account(self, account_id):
        self.choose_an_account.select_option(value=str(account_id))
        return self

    def enter_recipient_name(self, name):
        self.recipient_name.click()
        self.recipient_name.type(name, delay=50)
        expect(self.transfer_button).to_be_enabled()
        self.take_screenshot("recipient_name")
        return self

    def enter_recipient_account_number(self, account_number):
        self.recipient_account_number.click()
        self.recipient_account_number.type(account_number, delay=50)
        self.take_screenshot("recipient_account_number")
        return self

    def enter_amount(self, amount):
        self.fill_amount.click()
        self.fill_amount.type(str(amount))
        self.take_screenshot("fill_amount")
        return self

    def check(self):
        self.get_by_check.click()
        self.take_screenshot("check")
        return self

    def transfer(self, message):
        with self.check_alert_message_and_accept(message):
            self.transfer_button.click()
            return self

    def transfer_invalid_button(self, message):
        with self.page.expect_event("dialog") as dialog:
            yield
        self.current_alert_message = dialog.value.message

        assert message in self.current_alert_message, f"Incorrect error message: {self.current_alert_message}"
        dialog.value.accept()

    def transfer_expected_error(self, message):
        self._handle_alert_before_click(message=message, button_locator=self.transfer_button)
        return self

    def parse_transfer_alert(self):
        match = re.search(r"Successfully transferred \$([\d.]+)", self.current_alert_message)
        if match:
            self.transfer_amount = float(match.group(1))
        return self.transfer_amount
