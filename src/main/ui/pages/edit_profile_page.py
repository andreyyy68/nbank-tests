from src.main.ui.pages.base_page import BasePage
from playwright.sync_api import Page, expect

class EditProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.edit_profile = self.page.get_by_placeholder("Enter new name")
        self.button_save_changes = self.page.get_by_role("button", name="Save Changes")

    @property
    def url(self):
        return "/edit-profile"

    def edit_profile_name(self, name):
        self.edit_profile.fill(name)
        self.take_screenshot("edit_profile_name")
        return self

    def button_save_change(self, message):
        with self.check_alert_message_and_accept(message):
            self.page.evaluate("""
                      () => {
                          const btn = document.querySelector('button.btn.btn-primary.mt-3');
                          if (!btn) throw new Error('Button not found');
                          btn.click();
                      }
                  """)
        return self

    def button_expecting_error(self, message):
       self._handle_alert_before_click(message=message, button_locator=self.button_save_changes)
       return self












