from typing import List, Any
import allure

class BaseSteps:
    def __init__(self, created_objects: List[Any]):
        self.created_objects = created_objects

    def add_created_object(self, created_object: Any):
        with allure.step("Created object"):
           self.created_objects.append(created_object)

    def _attach_model(self, model, name: str):
        allure.attach(
            model.model_dump_json(indent=2, exclude_none=True),
            name=name,
            attachment_type=allure.attachment_type.JSON
        )