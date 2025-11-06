from abc import ABC, abstractmethod
from playwright.sync_api import Page, Dialog, expect
from src.main.configs.config import Config
from typing import TypeVar, Type, List
from contextlib import contextmanager
import allure



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
        self.h1 = self.page.locator("h1")

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
        self.page.reload()
        self.profile_name.wait_for(state="visible")
        assert self.profile_name.text_content()  == expected_name
        return self

    def get_welcome_text(self):
        self.h1.wait_for(state="visible", timeout=30000)
        text = self.h1.inner_text().strip()
        return text if text else None

    def take_screenshot(self, name: str):
        allure.attach(
            self.page.screenshot(),
            name=f"screenshot_filled_{name}",
            attachment_type=allure.attachment_type.PNG
        )

    def safe_click(self, locator):
        locator.wait_for(state="visible", timeout=10000)

        locator.scroll_into_view_if_needed()

        locator.wait_for(state="attached")

        try:
            locator.click(timeout=5000)
        except Exception:
            self.page.evaluate("el => el.click()", locator.element_handle())

        self.page.wait_for_timeout(500)