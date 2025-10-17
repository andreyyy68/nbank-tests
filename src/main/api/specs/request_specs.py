import logging
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.specs.response_specs import ResponseSpec

BASE_URL = 'http://localhost:4111/api/v1'
class RequestSpec:
    @staticmethod
    def default_req_headers():
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @staticmethod
    def unauth_spec():
        return RequestSpec.default_req_headers()

    @staticmethod
    def admin_auth_spec():
        headers = RequestSpec.default_req_headers()
        headers['Authorization'] = 'Basic YWRtaW46YWRtaW4='
        return headers

    @staticmethod
    def user_auth_spec(username: str, password: str):
        response = CrudRequester(
            RequestSpec.unauth_spec(),
            Endpoint.USER_AUTH,
            ResponseSpec.request_returns_ok(),
        ).post(LoginUserRequest(username=username, password=password))

        auth_header = response.headers.get('Authorization')
        if not auth_header:
            logging.error('No Authorization header in response')
            raise Exception('Failed to authenticate user')

        headers = RequestSpec.default_req_headers()
        headers['Authorization'] = auth_header
        return headers




