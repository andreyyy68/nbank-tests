from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps
from typing import List

class ApiManager:
    def __init__(self, created_object: List):
        self.admin_steps = AdminSteps(created_object)
        self.user_steps = UserSteps(created_object)