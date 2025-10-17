from src.main.api.models.base_model import BaseModel
from typing import List

class TransactionModel(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: str
    relatedAccountId: int

class DepositResponseModel(BaseModel):
    id: int
    accountNumber: str
    balance: int
    transactions: List[TransactionModel]

