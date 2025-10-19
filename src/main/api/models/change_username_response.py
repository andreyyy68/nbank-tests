from src.main.api.models.base_model import BaseModel
from typing import List, Any, Dict
from pydantic import RootModel

class CustomerModels(BaseModel):
    id: int
    username: str
    password: str
    name: str
    role: str
    accounts: List[Dict[str, Any]]

class ChangeUsernameResponse(BaseModel):
    customer: CustomerModels
    message: str

class CustomerResponseModel(RootModel):
    root: CustomerModels

