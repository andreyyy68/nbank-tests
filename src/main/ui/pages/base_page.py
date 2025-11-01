from abc import ABC, abstractmethod
from playwright.sync_api import Page, Dialog, expect
from src.main.configs.config import Config
from typing import TypeVar, Type, List
from contextlib import contextmanager



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
        self.profile_name = self.page.locator(".user-name")

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
    def check_alert_message_and_accept(self, expected_message: str):
        with self.page.expect_event("dialog") as dialog:
            yield
            self.current_alert_message = dialog.value.message
            assert expected_message in self.current_alert_message, f"Incorrect error message: {self.current_alert_message}"
            dialog.value.accept()

    def get_profile_name(self):
        self.page.reload()
        profile_reload_name = self.page.locator(".user-name")
        expect(profile_reload_name).not_to_have_text("")
        return profile_reload_name.text_content()

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

        if message:
            assert message in self.current_alert_message, f"Incorrect alert message: {self.current_alert_message}"

    def get_text(self, locator) -> str | None:
        try:
            return locator.text_content()
        except Exception:
            return None















