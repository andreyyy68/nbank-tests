from typing import List, Any
from src.main.api.fixtures.user_fixtures import *


@pytest.fixture
def created_objects():
    objects: List[Any] = []
    yield objects

# def cleanup_objects(objects: List[Any]):
#     api_manager = ApiManager(objects)
#     for obj in objects:
#         if isinstance(obj, CreateUserResponse):
#             api_manager.admin_steps.delete_user(obj.id)
#         else:
#             logging.warning(f'Object type: {type(obj)} is not deleted')