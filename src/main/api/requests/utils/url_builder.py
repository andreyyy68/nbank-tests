import re
from typing import Tuple, Dict
from src.main.api.configs.config import Config


class UrlBuilder:
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url

    def build(self, **params) -> Tuple[str, Dict]:
        for key, value in params.items():
            if not isinstance(value, (int, str)):
                raise ValueError(f"Parameter {key} must be int or str, got {type(value)}")

        backend = Config.get("backend_url")

        placeholders = re.findall(r"{(\w+)}", self.endpoint_url)
        url_params = {k: params.pop(k) for k in placeholders if k in params}

        missing = [p for p in placeholders if p not in url_params]
        if missing:
            raise ValueError(f"Missing URL parameters {missing} for endpoint: {self.endpoint_url}")

        url = self.endpoint_url.format(**url_params)

        query_params = params if params else None

        return f"{backend}{url}", query_params
