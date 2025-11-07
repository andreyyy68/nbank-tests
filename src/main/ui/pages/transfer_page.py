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

    def select_account(self, account_id, amount):
        option_selector = f"option[value='{account_id}']"
        for attempt in range(1, 5):
            if attempt > 1:
                self.page.reload(wait_until="networkidle")
            try:
                option = self.choose_an_account.locator(option_selector)
                text = option.text_content()
                match = re.search(r"Balance: \$([\d.]+)", text)
                if not match:
                    raise ValueError(f"Не удалось извлечь баланс из {text}")

                balance = float(match.group(1))
                if balance >= amount:
                  self.choose_an_account.select_option(value=str(account_id))
                  self.take_screenshot("choose_an_account")
                else:
                    self.page.reload()
                    self.choose_an_account.wait_for(state="attached")
            except AssertionError:
                raise "Баланс"

        return self

    def enter_recipient_name(self, name):
        self.recipient_name.fill(name)
        self.take_screenshot("recipient_name")
        return self

    def enter_recipient_account_number(self, account_number):
        self.recipient_account_number.fill(account_number)
        self.take_screenshot("recipient_account_number")
        return self

    def enter_amount(self, amount):
        self.fill_amount.fill(str(amount))
        self.take_screenshot("fill_amount")
        return self

    def check(self):
        self.get_by_check.click()
        self.take_screenshot("check")
        return self

    def transfer(self, message):
        self.page.wait_for_load_state("networkidle")
        expect(self.transfer_button).to_be_enabled(timeout=10000)
        self.page.wait_for_timeout(1500)

        with self.check_alert_message_and_accept(message, timeout=60000):
            self.transfer_button.click(force=True)
            self.page.wait_for_timeout(2000)
        return self

    def transfer_expected_error(self, message):
        self._handle_alert_before_click(message=message, button_locator=self.transfer_button)
        return self

    def parse_transfer_alert(self):
        match = re.search(r"Successfully transferred \$([\d.]+)", self.current_alert_message)
        if match:
            self.transfer_amount = float(match.group(1))
        return self.transfer_amount
