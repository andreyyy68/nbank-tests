from src.main.ui.elements.base_element import BaseElement


class UserBadgeElement(BaseElement):
    def __init__(self, locator):
        super().__init__(locator)
        self.username = None
        self.role = None

        try:
            locator.wait_for(state="visible")
            text = locator.inner_text()
        except:
            try:
                text = locator.evaluate("el => el.textContent").strip()
            except:
                text = None

        if text:
            parts = text.split()
            if len(parts) >= 2:
                self.username, self.role = parts[0], parts[1]