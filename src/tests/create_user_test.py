import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest




@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        'create_user_request', [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_valid_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        api_manager.admin_steps.create_user(user_request=create_user_request)
        response = api_manager.admin_steps.get_user(create_user_request.username)

        assert response.username == create_user_request.username
        assert response.role == create_user_request.role


        # Проблема при удалении
        # AdminUserRequester(
        #     RequestSpec.admin_auth_spec(),
        #     ResponseSpec.entity_was_deleted()
        # ).delete(create_user_response.id)

    @pytest.mark.parametrize(
        argnames='username, password, role, error_key, error_value',
        argvalues=[
            ('qwerty@', 'SDA<LDSALPDA><:D@"Q', 'USER', 'username', 'Username must contain only letters, digits, dashes, underscores, and dots'),
            ('qw', 'ru', 'USER', 'username', 'Username must be between 3 and 15 characters'),
            ('ababababababqwer', 'Asdqwertkfmxkda1', 'USER', 'username', 'Username must be between 3 and 15 characters')
        ]
    )

    def test_create_invalid_user(self, api_manager: ApiManager, username: str, password: str, role: str, error_key: str, error_value: str):
        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        api_manager.admin_steps.create_invalid_user(user_request=create_user_request, error_key=error_key, error_value=error_value)





