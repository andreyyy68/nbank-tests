import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.change_username import ChangeUsernameModel



class TestChangeUsername:
    @pytest.mark.debug
    def test_valid_change_username(self, api_manager: ApiManager, user_request):
        api_manager.user_steps.change_username(user_request)
        response = api_manager.user_steps.get_profile(user_request)

        assert response.username == user_request.username

    # Баг с изменением имени / 200 -> 404 / 400
    # Требования: Два слова, состоящее из букв, разделенные пробелом
    @pytest.mark.parametrize(
        argnames='name',
        argvalues=[
            ('N'),
            (' ')
        ]
    )

    def test_invalid_change_username(self, user_request, name, api_manager: ApiManager):
        change_user_request = ChangeUsernameModel(name=name)
        api_manager.user_steps.change_invalid_username(change_user_request, user_request)
        response = api_manager.user_steps.get_profile(user_request)

        assert response.username != name


