from src.main.api.models.base_model import BaseModel
from pydantic import RootModel
from typing import List, Optional

class TransactionModel(BaseModel):
    id: int
    amount: float
    relatedAccountId: int
    type: Optional[str] = None
    createdAt: Optional[str] = None


class TransactionsResponse(RootModel):
    root: List[TransactionModel]

    def __getitem__(self, index):
        return self.root[index]

    def __iter__(self):
        return iter(self.root)

