from typing import Annotated
from src.main.api.generators.generating_rule import GeneratingRule
from src.main.api.models.base_model import BaseModel
from src.main.configs.config import Config


class CreateUserRequest(BaseModel):
    username: Annotated[str, GeneratingRule(regex=r"^[A-Za-z0-9]{3,15}$")]
    password: Annotated[str, GeneratingRule(regex=r"^[A-Z]{3}[1-9]{1}[a-z]{3}[$%&]{2}")]
    role: Annotated[str, GeneratingRule(regex=r"^USER$")]

    @staticmethod
    def get_admin():
        return CreateUserRequest(username=Config.get('admin_account'), password=Config.get('admin_password'), role="ADMIN")
