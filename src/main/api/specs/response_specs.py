from http import HTTPStatus

from requests import Response
from typing import Callable
from json import JSONDecodeError


class ResponseSpec:
    @staticmethod
    def request_returns_ok() -> Callable:
        def check(response: Response):
           assert response.status_code == HTTPStatus.OK, response.text
        return check

    @staticmethod
    def entity_was_created() -> Callable:
        def check(response: Response):
           assert response.status_code == HTTPStatus.CREATED, response.text
        return check

    @staticmethod
    def entity_was_deleted() -> Callable:
        def check(response: Response):
            assert response.status_code in [HTTPStatus.NO_CONTENT, HTTPStatus.OK], response.text
        return check


    @staticmethod
    def request_returns_bad_request(error_key: str, error_value: str) -> Callable:
        def check(response: Response):
           assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
           if error_key is not None and error_value is not None:
               try:
                   data = response.json()
                   assert error_value in data.get(error_key, None)
               except JSONDecodeError:
                   pass
        return check

    @staticmethod
    def response_expected_status_balance(expected_status: int, expected_balance) -> Callable:
        def check(response: Response):
            assert response.status_code == expected_status
            if expected_status == HTTPStatus.OK:
                json_data = response.json()
                assert json_data['balance'] == expected_balance
        return check

    @staticmethod
    def forbidden() -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN
        return check

    @staticmethod
    def response_expected_status(expected_status) -> Callable:
        def check(response: Response):
            assert response.status_code == expected_status, response.text
        return check





