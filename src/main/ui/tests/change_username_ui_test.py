import pytest
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.change_username import ChangeUsernameModel
from src.main.ui.constants.alert_message import AlertMessage
from src.main.ui.pages.edit_profile_page import EditProfilePage
from src.main.ui.constants.defaults import DefaultValues


@pytest.mark.regression
@pytest.mark.ui
class TestChangeUsername:
    @pytest.mark.parametrize("data_user",
                             [(RandomModelGenerator.generate(ChangeUsernameModel))])
    def test_valid_change_username(self, user_page, api_manager, data_user):
        EditProfilePage(user_page).open().edit_profile_name(data_user.name).button_save_change(AlertMessage.NAME_UPDATE).get_profile_name(data_user.name)


        username = api_manager.user_steps.get_changed_username()
        assert username, "The name has not changed on BE"

    def test_invalid_change_username(self, user_page, api_manager):
        EditProfilePage(user_page).open().button_expecting_error(AlertMessage.NAME_UPDATED_FAILED).get_profile_name(DefaultValues.NONAME)

        current_username = api_manager.user_steps.get_changed_username()
        assert not current_username, "The name has changed on BE"