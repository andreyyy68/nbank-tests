from src.main.fixtures.user_fixtures import user_account
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.change_username import ChangeUsernameModel
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequestModel
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.transaction_type import TransactionType
from src.main.api.models.transfer_money_model import TransferMoneyRequest
from src.main.api.models.user_account import UserAccount
from src.main.api.models.user_two_accounts import UserTwoAccounts
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpec
from src.main.api.specs.response_specs import ResponseSpec
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.requests.skeleton.endpoint import Endpoint
from typing import Optional, List, Any
import allure




class UserSteps(BaseSteps):
    def __init__(self, created_object: List[Any]):
        super().__init__(created_object)
        self.user = None

    def set_user(self, user: CreateUserRequest):
        self.user = user
        return self

    @staticmethod
    def _user_must_be_set(func):
        def wrapper(self, *args, **kwargs):
            assert self.user is not None, "User must be set before calling this step"
            return func(self, *args, **kwargs)

        return wrapper

    def login(self):
        with allure.step(f"User Login, body:{self.user}"):
            login_user_request = LoginUserRequest(username=self.user.username, password=self.user.password)
            login_response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(login_user_request.username, login_user_request.password),
                Endpoint.USER_AUTH,
                ResponseSpec.request_returns_ok()
            ).post(login_user_request)

            ModelAssertions(login_user_request, login_response).match()

            self.created_objects.append(login_response)

            return login_response


    def create_account(self) -> CreateAccountResponse:
        with allure.step(f"User create account, body:{self.user}"):
            LoginUserRequest(username=self.user.username, password=self.user.password)
            create_account_response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpec.entity_was_created()
            ).post()

            assert create_account_response.balance == 0.0
            assert not create_account_response.transactions
            return create_account_response


    def change_username(self):
        with allure.step(f"User change username, body:{self.user}"):
            change_user_request = RandomModelGenerator.generate(ChangeUsernameModel)
            ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.CHANGE_USERNAME,
                ResponseSpec.request_returns_ok()
            ).update(change_user_request)


    def change_invalid_username(self, invalid_user_request: ChangeUsernameModel):
        with allure.step(f"User invalid change username, body:{self.user}"):
            CrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.CHANGE_USERNAME,
                ResponseSpec.request_returns_bad_request(error_key="error", error_value="Name must contain two words with letters only")
            ).update(invalid_user_request)


    def deposit_user(self, user_account_id, request_balance: Optional[int] = None):
        with allure.step(f"User deposit, body:{self.user}"):
            request = DepositRequestModel(id=user_account_id, balance=request_balance)
            response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.USER_DEPOSIT,
                ResponseSpec.request_returns_ok()
            ).post(request)

            ModelAssertions(request, response).match()


    def invalid_deposit_user(self, user_account_id, request_balance: int | float, expected_status):
        with allure.step(f"User invalid deposit, body:{self.user}, account id:{user_account_id}, balance:{request_balance}"):
            request = DepositRequestModel(id=user_account_id, balance=request_balance)
            CrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.USER_DEPOSIT,
                ResponseSpec.response_expected_status(expected_status)
            ).post(request)


    def deposit_invalid_id_user(self, request_balance: int):
        with allure.step(f"User invalid deposit, body:{self.user}, balance:{request_balance}"):
            request = DepositRequestModel(
                id=4444,
                balance=request_balance
            )
            CrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.USER_DEPOSIT,
                ResponseSpec.forbidden()
            ).post(request)


    def transfer_between_your_accounts(self, user_with_two_accounts: UserTwoAccounts, amount: Optional[int] = None):
        with allure.step(f"User transfer, body:{self.user}, sender account id:{user_with_two_accounts.from_account_id},"
                         f"receiver account id:{user_with_two_accounts.to_account_id}, amount:{amount}"):
            request = TransferMoneyRequest(
                senderAccountId=user_with_two_accounts.from_account_id,
                receiverAccountId=user_with_two_accounts.to_account_id,
                amount=amount
            )
            ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=user_with_two_accounts.user.username,
                                           password=user_with_two_accounts.user.password),
                Endpoint.TRANSFER,
                ResponseSpec.request_returns_ok()
            ).post(request)
            ModelAssertions(request, request).match()


    def transfer_between_invalid_your_accounts(self, user_with_two_accounts: UserTwoAccounts, amount, expected_status):
        with allure.step(f"User invalid transfer between, body:{self.user}, sender account id:{user_with_two_accounts.from_account_id},"
                        f"receiver account id:{user_with_two_accounts.to_account_id}, amount:{amount}"):
            request = TransferMoneyRequest(
                senderAccountId=user_with_two_accounts.from_account_id,
                receiverAccountId=user_with_two_accounts.to_account_id,
                amount=amount
            )
            CrudRequester(
                RequestSpec.user_auth_spec(username=user_with_two_accounts.user.username,
                                           password=user_with_two_accounts.user.password),
                Endpoint.TRANSFER,
                ResponseSpec.response_expected_status(expected_status)
            ).post(request)
            ModelAssertions(request, request).match()


    def get_transactions(self, account_id):
        with allure.step(f"User get transactions, body:{self.user}, account id:{account_id}"):
            response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.GET_TRANSACTIONS,
                ResponseSpec.request_returns_ok()
            ).get(accountId=account_id)

            return response


    def get_transactions_between_your_accounts(self, user_with_two_accounts: UserTwoAccounts):
        with allure.step(f"User get transactions, body:{self.user}, account id:{user_with_two_accounts.from_account_id},"):
            response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=user_with_two_accounts.user.username,
                                           password=user_with_two_accounts.user.password),
                Endpoint.GET_TRANSACTIONS,
                ResponseSpec.request_returns_ok()
            ).get(accountId=user_with_two_accounts.from_account_id)

            transactions = [
                transaction for transaction in response if transaction.type == TransactionType.TRANSFER.value
            ]
            return transactions


    def get_account(self, user_account: UserAccount):
        with allure.step(f"User get account, body:{self.user}, account:{user_account}"):
            response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.GET_ACCOUNT,
                ResponseSpec.request_returns_ok()
            ).get()
            account = next(acc for acc in response if acc.id == user_account.account_id)

            return account


    def get_profile(self):
        with allure.step(f"USer get profile, body:{self.user}"):
            response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.GET_PROFILE,
                ResponseSpec.request_returns_ok()
            ).get()

            return response.root


    def get_auth_token(self):
        with allure.step(f"Get auth token, body:{self.user}"):
            login_request = LoginUserRequest(username=self.user.username, password=self.user.password)
            response = CrudRequester(
                RequestSpec.unauth_spec(),
                Endpoint.USER_AUTH,
                ResponseSpec.request_returns_ok()
            ).post(login_request)

            return response.headers.get('Authorization')


    def get_account_number(self, account_number):
        with allure.step(f"User get account number, body:{self.user}, account number:{account_number}"):
            response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.GET_ACCOUNT,
                ResponseSpec.request_returns_ok()
            ).get()

            account = next(acc for acc in response if acc.accountNumber == account_number)
            return account


    def get_changed_username(self):
        with allure.step(f"User get changed username, body:{self.user}"):
            response = ValidatedCrudRequester(
                RequestSpec.user_auth_spec(username=self.user.username, password=self.user.password),
                Endpoint.GET_PROFILE,
                ResponseSpec.request_returns_ok()
            ).get()

            return response.root.name


















