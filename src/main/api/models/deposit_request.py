from src.main.api.models.base_model import BaseModel

class DepositRequestModel(BaseModel):
    id: int
    balance: int