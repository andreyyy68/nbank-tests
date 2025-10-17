from src.main.api.classes.api_manager import ApiManager
import pytest



@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager: ApiManager, user_request):
        api_manager.user_steps.create_account(user_request)