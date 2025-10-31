from src.main.ui.elements.base_element import BaseElement


class UserBadgeElement(BaseElement):
    def __init__(self, locator):
        super().__init__(locator)
        self.username = None
        self.role = None

        try:
            locator.wait_for(state="visible")
            self.username, self.role = locator.inner_text().split()
        except:
            pass