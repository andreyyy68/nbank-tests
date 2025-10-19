from src.main.api.fixtures.user_fixtures import user_account
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.change_username import ChangeUsernameModel
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequestModel
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.transfer_money_model import TransferMoneyRequest
from src.main.api.models.user_account import UserAccount
from src.main.api.models.user_two_accounts import UserTwoAccounts
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpec
from src.main.api.specs.response_specs import ResponseSpec
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.requests.skeleton.endpoint import Endpoint
from typing import Optional



class UserSteps(BaseSteps):
    def login(self, user_request: CreateUserRequest):
        login_user_request = LoginUserRequest(username=user_request.username, password=user_request.password)
        login_response = ValidatedCrudRequester(
            RequestSpec.user_auth_spec(login_user_request.username, login_user_request.password),
            Endpoint.USER_AUTH,
            ResponseSpec.request_returns_ok()
        ).post(login_user_request)

        ModelAssertions(login_user_request, login_response).match()

        self.created_objects.append(login_response)

        return login_response

    def create_account(self, user_request: CreateUserRequest) -> CreateAccountResponse:
        LoginUserRequest(username=user_request.username, password=user_request.password)
        create_account_response = ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_request.username, password=user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpec.entity_was_created()
        ).post()

        assert create_account_response.balance == 0.0
        assert not create_account_response.transactions
        return create_account_response

    def change_username(self, user_request: CreateUserRequest):
        change_user_request = RandomModelGenerator.generate(ChangeUsernameModel)
        ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_request.username, password=user_request.password),
            Endpoint.CHANGE_USERNAME,
            ResponseSpec.request_returns_ok()
        ).update(change_user_request)


    def change_invalid_username(self, invalud_user_request: ChangeUsernameModel, user_request: CreateUserRequest):
        ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_request.username, password=user_request.password),
            Endpoint.CHANGE_USERNAME,
            ResponseSpec.request_returns_ok()
        ).update(invalud_user_request)

    def deposit_user(self, user_account, request_balance: Optional[int] = None):
        request = DepositRequestModel(id=user_account.account_id, balance=request_balance)
        response = ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_account.user.username, password=user_account.user.password),
            Endpoint.USER_DEPOSIT,
            ResponseSpec.request_returns_ok()
        ).post(request)

        ModelAssertions(request, response).match()

    def invalid_deposit_user(self, user_account, request_balance: int | float, expected_status):
        request = DepositRequestModel(id=user_account.account_id, balance=request_balance)
        CrudRequester(
            RequestSpec.user_auth_spec(username=user_account.user.username, password=user_account.user.password),
            Endpoint.USER_DEPOSIT,
            ResponseSpec.response_expected_status(expected_status)
        ).post(request)

    def deposit_ivalid_id_user(self, user_request, request_balance: int):
        request = DepositRequestModel(
            id=4444,
            balance=request_balance
        )
        CrudRequester(
            RequestSpec.user_auth_spec(username=user_request.username, password=user_request.password),
            Endpoint.USER_DEPOSIT,
            ResponseSpec.forbidden()
        ).post(request)

    def transfer_between_your_accounts(self, user_with_two_accounts: UserTwoAccounts, amount: Optional[int] = None):
        request = TransferMoneyRequest(
            senderAccountId = user_with_two_accounts.from_account_id,
            receiverAccountId =user_with_two_accounts.to_account_id,
            amount = amount
        )
        ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_with_two_accounts.user.username, password=user_with_two_accounts.user.password),
            Endpoint.TRANSFER,
            ResponseSpec.request_returns_ok()
        ).post(request)
        ModelAssertions(request, request).match()

    def transfer_between_invalid_your_accounts(self, user_with_two_accounts: UserTwoAccounts, amount, expected_status):
        request = TransferMoneyRequest(
            senderAccountId=user_with_two_accounts.from_account_id,
            receiverAccountId=user_with_two_accounts.to_account_id,
            amount=amount
        )
        CrudRequester(
            RequestSpec.user_auth_spec(username=user_with_two_accounts.user.username, password=user_with_two_accounts.user.password),
            Endpoint.TRANSFER,
            ResponseSpec.response_expected_status(expected_status)
        ).post(request)
        ModelAssertions(request, request).match()

    def get_transactions(self, user_account: UserAccount):
        response = ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_account.user.username, password=user_account.user.password),
            Endpoint.GET_TRANSACTIONS,
            ResponseSpec.request_returns_ok()
        ).get(accountId=user_account.account_id)

        return response

    def get_transactions_between_your_accounts(self, user_with_two_accounts: UserTwoAccounts):
        response = ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_with_two_accounts.user.username, password=user_with_two_accounts.user.password),
            Endpoint.GET_TRANSACTIONS,
            ResponseSpec.request_returns_ok()
        ).get(accountId=user_with_two_accounts.from_account_id)

        return response

    def get_account(self, user_account: UserAccount):
        response = ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_account.user.username, password=user_account.user.password),
            Endpoint.GET_ACCOUNT,
            ResponseSpec.request_returns_ok()
        ).get()
        account = next(acc for acc in response if acc.id == user_account.account_id)

        return account

    def get_profile(self, user_request: CreateUserRequest):
        response = ValidatedCrudRequester(
            RequestSpec.user_auth_spec(username=user_request.username, password=user_request.password),
            Endpoint.GET_PROFILE,
            ResponseSpec.request_returns_ok()
        ).get()

        return response.root

















