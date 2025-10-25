import pytest
from src.main.classes.api_manager import ApiManager
from src.main.api.models.login_user_request import LoginUserRequest



class TestLoginUser:
    @pytest.mark.usefixtures("user_request", "api_manager")
    def test_login_user(self, user_request, api_manager: ApiManager):
        api_manager.user_steps.set_user(user_request).login()

    @pytest.mark.usefixtures("api_manager")
    def test_login_admin_user(self, api_manager: ApiManager, admin_user_request: LoginUserRequest):
        api_manager.user_steps.set_user(admin_user_request).login()




