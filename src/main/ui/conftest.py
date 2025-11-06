import pytest
from playwright.sync_api import Browser, Playwright
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.helpers.context import add_item_to_local_storage
from src.main.classes.api_manager import ApiManager
from src.main.configs.config import Config
import allure
import time


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": Config.get("ui_base_url"),
    }

@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True, slow_mo=50)
    yield browser
    browser.close()

@pytest.fixture
def new_context(browser: Browser, browser_context_args):
    context = browser.new_context(**browser_context_args, record_video_dir="test-output/videos")
    yield context
    for idx, page in enumerate(context.pages, start=1):
        try:
            page.close()
        except Exception:
            pass
        try:
            video_path = page.video.path()
            timestamp = int(time.time() * 1000)
            allure.attach.file(
                video_path,
                name=f"video_{idx}_{timestamp}.webm",
                attachment_type=allure.attachment_type.WEBM
            )
        except Exception:
            pass

    context.close()

@pytest.fixture
def new_page(new_context):
    yield new_context.new_page()


@pytest.fixture(scope="function")
def admin_token(api_manager: ApiManager):
    return api_manager.user_steps.set_user(CreateUserRequest.get_admin()).get_auth_token()


@pytest.fixture(scope="function")
def user_token(api_manager: ApiManager, user_request):
    return api_manager.user_steps.set_user(user_request).get_auth_token()


@pytest.fixture
def admin_session(new_context, admin_token):
    add_item_to_local_storage(
        context=new_context,
        item_key="authToken",
        item_value=admin_token,
    )
    yield new_context


@pytest.fixture
def user_session(new_context, user_token):
    add_item_to_local_storage(
        context=new_context,
        item_key="authToken",
        item_value=user_token,
    )
    yield new_context


@pytest.fixture
def admin_page(admin_session):
    page = admin_session.new_page()
    yield page
    page.close()


@pytest.fixture
def user_page(user_session):
    page = user_session.new_page()
    yield page
    page.close()







