import pytest
from src.main.ui.pages.user_dashboard_page import UserDashboardPage


@pytest.mark.ui
class TestCreateUserAccount:
    def test_user_create_account(self, user_page, api_manager):
        account_number = UserDashboardPage(user_page).open().create_account_and_get_account_number()
        account = api_manager.user_steps.get_account_number(account_number)
        assert account, "Could not find new account on BE"