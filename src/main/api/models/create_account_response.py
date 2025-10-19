from src.main.api.models.base_model import BaseModel
from typing import List
from pydantic import RootModel

class CreateAccountResponse(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: List

class AccountResponseModel(RootModel):
    root : List[CreateAccountResponse]

    def __iter__(self):
        return iter(self.root)