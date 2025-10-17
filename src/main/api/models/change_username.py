from typing import Annotated
from src.main.api.generators.generating_rule import GeneratingRule
from src.main.api.models.base_model import BaseModel

class ChangeUsernameModel(BaseModel):
    name: Annotated[str, GeneratingRule(regex=r"^[A-Za-z]{3,10} [A-Za-z]{3,10}$")]