from dataclasses import dataclass
from src.main.api.models.create_user_request import CreateUserRequest


@dataclass
class UserAccount:
    user: CreateUserRequest
    account_id: int