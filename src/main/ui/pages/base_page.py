from abc import ABC, abstractmethod
from playwright.sync_api import Page, Dialog, expect
from src.main.configs.config import Config
from typing import TypeVar, Type, List
from contextlib import contextmanager
import allure
import re


T = TypeVar('T', bound='BasePage')
E = TypeVar('E', bound='BaseElement')

class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        self.username_field = self.page.get_by_placeholder('Username')
        self.password_field = self.page.get_by_placeholder('Password')
        self.choose_an_account = self.page.locator("select.form-control.account-selector")
        self.fill_amount = self.page.get_by_placeholder("Enter amount")
        self.base_url = Config.get('ui_base_url')
        self.get_by_check = self.page.locator("#confirmCheck")
        self.profile_name = self.page.locator(".user-info .user-name")
        self.welcome_text = page.locator(".welcome-text")
        self.edit_profile = self.page.get_by_placeholder("Enter new name")

        self.current_alert_message = None
        self.deposit_amount = None
        self.transfer_amount = None

    @property
    @abstractmethod
    def url(self):...

    def open(self):
        full_url = f'{self.base_url}{self.url}'
        self.page.goto(full_url)
        return self

    def get_page(self, page_class: Type[T]) -> T:
        return page_class(self.page)

    @staticmethod
    def get_page_elements(locator, page_element_class: Type[E]) -> List[E]:
        return [page_element_class(locator) for locator in locator.all()]

    @contextmanager
    def check_alert_message_and_accept(self, expected_message: str, timeout=30000):
        with self.page.expect_event("dialog", timeout=timeout) as dialog:
            yield
            self.current_alert_message = dialog.value.message
            allure.attach(
                f"Alert message: {dialog.value.message}",
                name="alert_text",
                attachment_type=allure.attachment_type.TEXT
            )
            assert expected_message in self.current_alert_message, f"Incorrect error message: {self.current_alert_message}"
            dialog.value.accept()

    def check_redirect_to(self, expected_url: str):
        self.page.wait_for_url(expected_url)
        return self

    def _handle_alert_before_click(self, message: str, button_locator = None):
        def dialog_handler(dialog: Dialog):
            self.current_alert_message = dialog.message
            dialog.accept()

        self.page.once("dialog", dialog_handler)

        if button_locator:
            button_locator.click()

        self.take_screenshot("button_expecting_error")

        if message:
            assert message in self.current_alert_message, f"Incorrect alert message: {self.current_alert_message}"

    def get_text(self, locator) -> str | None:
        try:
            return locator.text_content()
        except Exception:
            return None

    def get_profile_name(self, expected_name):
        try:
            expect(self.profile_name).to_have_text(expected_name, timeout=3000)
            return self
        except AssertionError:
            pass

        for attempt in range(1, 4):
            self.page.reload(wait_until="networkidle", timeout=30000)
            self.profile_name.wait_for(state="visible", timeout=5000)

            try:
                expect(self.profile_name).to_have_text(re.compile(expected_name, re.IGNORECASE), timeout=3000)
                return self
            except AssertionError:
                if attempt == 3:
                    actual = self.profile_name.text_content()
                    self.page.screenshot(path="/app/test-output/profile-error.png")
                    raise AssertionError(
                        f"Expected '{expected_name}', got '{actual}' after 3 retries"
                    )

    def get_welcome_text(self):
        self.welcome_text.wait_for(state="attached", timeout=60000)
        self.take_screenshot("user_dashboard")
        return self.welcome_text.text_content()

    def take_screenshot(self, name: str):
        allure.attach(
            self.page.screenshot(),
            name=f"screenshot_filled_{name}",
            attachment_type=allure.attachment_type.PNG
        )

    def refresh(self):
        self.page.reload()
        return self

    def safe_accept_existing_dialogs(self):
        try:
            with self.page.expect_event("dialog", timeout=1000) as d:
                pass
            d.value.accept()
        except:
            pass
        return self


