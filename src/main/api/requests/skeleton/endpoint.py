from src.main.api.models.base_model import BaseModel
from dataclasses import dataclass
from typing import Type
from enum import Enum
from src.main.api.models.change_username import ChangeUsernameModel
from src.main.api.models.change_username_response import ChangeUsernameResponse, CustomerResponseModel
from src.main.api.models.create_account_response import CreateAccountResponse, AccountResponseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse, UserResponseModel
from src.main.api.models.deposit_request import DepositRequestModel
from src.main.api.models.deposit_response import DepositResponseModel
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transactions_model import TransactionsResponse
from src.main.api.models.transfer_money_model import TransferMoneyRequest
from src.main.api.models.transfer_money_response import TransferMoneyResponse



@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: Type[BaseModel] | None
    response_model: Type[BaseModel] | None

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfig(
        url='/admin/users',
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfig(
        url='/admin/users/delete',
        request_model=None,
        response_model=None
    )

    USER_AUTH = EndpointConfig(
        url='/auth/login',
        request_model=LoginUserRequest,
        response_model=LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfig(
        url='/accounts',
        request_model = None,
        response_model=CreateAccountResponse
    )

    CHANGE_USERNAME = EndpointConfig(
        url='/customer/profile',
        request_model = ChangeUsernameModel,
        response_model=ChangeUsernameResponse
    )

    USER_DEPOSIT = EndpointConfig(
        url = '/accounts/deposit',
        request_model=DepositRequestModel,
        response_model=DepositResponseModel
    )

    TRANSFER = EndpointConfig(
        url = '/accounts/transfer',
        request_model=TransferMoneyRequest,
        response_model=TransferMoneyResponse
    )

    GET_TRANSACTIONS = EndpointConfig(
        url = '/accounts/{accountId}/transactions',
        request_model = None,
        response_model = TransactionsResponse
    )

    GET_USER = EndpointConfig(
        url = '/admin/users',
        request_model = None,
        response_model=UserResponseModel
    )

    GET_ACCOUNT = EndpointConfig(
        url = '/customer/accounts',
        request_model = None,
        response_model=AccountResponseModel
    )

    GET_PROFILE = EndpointConfig(
        url = '/customer/profile',
        request_model = None,
        response_model = CustomerResponseModel
    )

