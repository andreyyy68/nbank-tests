import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.admin_panel_page import AdminPanelPage
from src.main.ui.constants.alert_message import AlertMessage



@pytest.mark.regression
@pytest.mark.ui
class TestCreateUser:
    @pytest.mark.parametrize("create_user_request", [RandomModelGenerator.generate(CreateUserRequest)])
    def test_admin_can_create_user(self, api_manager, admin_page, create_user_request):
        (AdminPanelPage(admin_page).open().
         create_user(username=create_user_request.username, password=create_user_request.password, message=AlertMessage.USER_CREATED).
         find_user_by_request(create_user_request))

        user = api_manager.admin_steps.get_user(create_user_request.username)
        assert user, "User was not created on BE"
        api_manager.admin_steps.add_created_object(user)

    def test_admin_can_not_create_user_with_invalid_data(self, api_manager, admin_page):
        user_data = RandomModelGenerator.generate(CreateUserRequest)
        username = RandomData.generate_username()
        admin_create_user_page = AdminPanelPage(admin_page).open(). create_user(username=username, password=user_data.password, message=AlertMessage.USER_CREATED_FAILED)

        ui_user = admin_create_user_page.find_user_by_username(user_data.username)
        assert not ui_user, "Found user in UI"

        user = api_manager.admin_steps.get_user(user_data.username)
        assert not user, "User was created on BE"