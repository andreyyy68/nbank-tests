from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpec
from src.main.api.specs.response_specs import ResponseSpec
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.requests.skeleton.endpoint import Endpoint


class AdminSteps(BaseSteps):
    def create_user(self, user_request: CreateUserRequest):
        create_user_response= ValidatedCrudRequester(
            RequestSpec.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpec.entity_was_created(),
        ).post(user_request)
        ModelAssertions(user_request, create_user_response).match()

        self.created_objects.append(create_user_response)

        return create_user_response

    def create_invalid_user(self, user_request: CreateUserRequest, error_key: str, error_value: str):
        CrudRequester(
            RequestSpec.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpec.request_returns_bad_request(error_key, error_value),
        ).post(user_request)

    def delete_user(self, user_id: int):
        pass
        # AdminUserRequester(
        #     RequestSpec.admin_auth_spec(),
        #     ResponseSpec.entity_was_deleted()
        # ).delete(user_id)




