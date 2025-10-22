from typing import Optional, List, Dict, Any
from src.main.api.models.base_model import BaseModel
from pydantic import RootModel


class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    name: Optional[str]
    role: str
    accounts: List[Dict[str, Any]]

class UserResponseModel(RootModel):
    root : List[CreateUserResponse]

    def __iter__(self):
        return iter(self.root)