from dataclasses import dataclass

from src.main.api.models.create_user_request import CreateUserRequest

@dataclass
class UserTwoAccounts:
    user: CreateUserRequest
    from_account_id: int
    to_account_id: int
    balance: float

