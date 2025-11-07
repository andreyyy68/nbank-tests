from src.main.classes.api_manager import ApiManager
import pytest


@pytest.fixture
def api_manager(created_objects):
    return ApiManager(created_objects)
