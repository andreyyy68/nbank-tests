from src.main.api.classes.api_manager import ApiManager
import pytest
from src.main.api.models.user_account import UserAccount


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager: ApiManager, user_request, user_account: UserAccount):
        api_manager.user_steps.create_account(user_request)
        response = api_manager.user_steps.get_account(user_account)

        assert response.id == user_account.account_id
        assert response.balance == 0
        assert response.transactions == []
