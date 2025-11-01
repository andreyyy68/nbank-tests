from src.main.ui.elements.base_element import BaseElement


class UserBadgeElement(BaseElement):
    def __init__(self, locator):
        super().__init__(locator)
        self.username = None
        self.role = None
        self.text = None

        for _ in range(10):
            try:
                locator.wait_for(state="visible")
                self.text = locator.inner_text().strip()
            except:
                self.text = None

            if self.text:
                break
        else:
            try:
                self.text = locator.evaluate("el => el.textContent").strip()
            except:
                self.text = None

        if self.text:
            parts = self.text.split()
            if len(parts) >= 2:
                self.username, self.role = parts[0], parts[1]