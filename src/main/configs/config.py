from pathlib import Path
from typing import Any


class Config:
    _isinstance = None
    _properties = {}

    def __new__(cls):
        if cls._isinstance is None:
            cls._isinstance = super(Config, cls).__new__(cls)
            config_path = Path(__file__).parents[3] / 'resources' / 'config.properties'
            if not config_path.exists():
                raise ImportError(f'{config_path} not found')
            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        cls._properties[key] = value
        return cls._isinstance

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        if Config._isinstance is None:
            Config()
        return Config._properties.get(key, default)


