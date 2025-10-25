import pytest
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.user_account import UserAccount
from src.main.api.models.user_two_accounts import UserTwoAccounts


@pytest.fixture
def user_request(api_manager):
    user_data = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_data)
    return user_data

@pytest.fixture
def admin_user_request(api_manager):
    return LoginUserRequest(username='admin', password='admin')

@pytest.fixture
def user_account(api_manager, user_request) -> UserAccount:
    account_id = api_manager.user_steps.set_user(user_request).create_account()
    return UserAccount(user=user_request, account_id=account_id.id)

@pytest.fixture
def user_with_two_accounts(api_manager, user_request) -> UserTwoAccounts:
    api_manager.user_steps.set_user(user_request)
    from_account = api_manager.user_steps.create_account()
    to_account = api_manager.user_steps.create_account()

    api_manager.user_steps.deposit_user(
        from_account.id,
        5555
    )

    return UserTwoAccounts(
        user=user_request,
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        balance=15,
    )

@pytest.fixture
def two_user_accounts(api_manager) -> UserTwoAccounts:
    from_user_data = RandomModelGenerator.generate(CreateUserRequest)
    to_user_data = RandomModelGenerator.generate(CreateUserRequest)

    api_manager.user_steps.create_user(from_user_data)
    api_manager.user_steps.create_user(to_user_data)

    from_account = api_manager.user_steps.create_account(from_user_data)
    to_account = api_manager.user_steps.create_account(to_user_data)

    api_manager.user_steps.deposit_user(
        user_account=UserAccount(user=from_user_data, account_id=from_account.id),
        request_balance=5000
    )

    return UserTwoAccounts(
        user=from_user_data,
        from_account_id=from_account.id,
        to_account_id=to_account.id,
    )








