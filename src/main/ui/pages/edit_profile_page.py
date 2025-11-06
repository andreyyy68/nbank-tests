from src.main.ui.pages.base_page import BasePage
from playwright.sync_api import Page, expect

class EditProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_save_changes = self.page.get_by_role("button", name="💾 Save Changes")

    @property
    def url(self):
        return "/edit-profile"

    def edit_profile_name(self, name):
        self.edit_profile.fill(name)
        expect(self.edit_profile).to_have_value(name, timeout=10000)
        self.take_screenshot("edit_profile_name")
        return self

    def button_save_change(self, message):
        with self.check_alert_message_and_accept(message):
            self.button_save_changes.wait_for(timeout=15000)
            expect(self.button_save_changes).to_be_enabled(timeout=15000)
            self.button_save_changes.click()
        return self

    def button_expecting_error(self, message):
       self._handle_alert_before_click(message=message, button_locator=self.button_save_changes)
       return self
