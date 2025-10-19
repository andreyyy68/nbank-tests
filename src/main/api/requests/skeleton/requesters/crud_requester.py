import requests
from typing import TypeVar, Optional, Generic
from pydantic import RootModel
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interface.crud_end_interface import CrudEndpointInterface
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.utils.url_builder import UrlBuilder



T = TypeVar("T", bound=BaseModel | RootModel)

class CrudRequester(HttpRequest, CrudEndpointInterface, Generic[T]):
    def _request(self, method: str, model: Optional[T] = None, **params) -> requests.Response:
        url, query_params = UrlBuilder(self.endpoint.value.url).build(**params)
        body = model.model_dump() if model else None

        response = requests.request(
            method=method,
            url=url,
            headers=self.request_spec,
            json=body,
            params=query_params
        )
        self.response_spec(response)
        return response

    def post(self, model: Optional[T] = None, **params) -> requests.Response:
        return self._request("POST", model, **params)

    def get(self, model: Optional[BaseModel | RootModel] = None, **params) -> requests.Response:
        return self._request("GET", **params)

    def put(self, model: Optional[T] = None,  **params) -> requests.Response:
        return self._request("PUT", model, **params)

    # def delete(self, **params) -> requests.Response:
    #     return self._request("DELETE", **params)
