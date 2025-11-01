from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.constants.defaults import DefaultValues
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.admin_panel_page import AdminPanelPage
from src.main.ui.pages.user_dashboard_page import UserDashboardPage
import pytest


@pytest.mark.regression
@pytest.mark.ui
class TestLoginUser:
    def test_login_admin(self, new_page):
        admin = CreateUserRequest.get_admin()
        admin_panel_page = LoginPage(new_page).open().login(admin.username, admin.password).get_page(AdminPanelPage)
        assert admin_panel_page.get_text_admin_panel() == "Admin Panel"

    def test_login_user(self, new_page, user_request):
        user_dashboard = LoginPage(new_page).open().login(user_request.username, user_request.password).get_page(UserDashboardPage)
        assert user_dashboard.get_text_user_dashboard() == "User Dashboard"
        assert user_dashboard.get_welcome_text() == DefaultValues.WELCOME_NONAME