import requests
from typing import TypeVar, Optional
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interface.crud_end_interface import CrudEndpointInterface
from src.main.api.models.base_model import BaseModel
from src.main.api.configs.config import Config


T = TypeVar('T', bound=BaseModel)
class CrudRequester(HttpRequest, CrudEndpointInterface):
    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''

        response = requests.post(
            url = f"{Config.get('backend_url')}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body
        )

        self.response_spec(response)
        return response

    # def get(self, id: int) -> Optional[T]:...

    def put(self, model: Optional[T], id: Optional[int] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''

        response = requests.put(
            url=f'{Config.get('backend_url')}{self.endpoint.value.url}',
            headers=self.request_spec,
            json=body,
        )
        self.response_spec(response)
        return response

    # def delete(self, id: int):
    #     response = requests.delete()