import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.login_user_request import LoginUserRequest



class TestLoginUser:
    @pytest.mark.usefixtures("user_request", "api_manager")
    def test_login_user(self, user_request, api_manager: ApiManager):
        api_manager.user_steps.login(user_request)

    @pytest.mark.usefixtures("api_manager")
    def test_login_admin_user(self, api_manager: ApiManager, admin_user_request: LoginUserRequest):
        api_manager.user_steps.login(admin_user_request)




