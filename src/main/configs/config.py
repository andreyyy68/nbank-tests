import os
import sys
from pathlib import Path
from typing import Any


class Config:
    _instance = None
    _properties = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._load_properties()
        return cls._instance

    @classmethod
    def _load_properties(cls):
        config_path = Path(__file__).parents[3] / 'resources' / 'config.properties'
        if config_path.exists():
            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith("#"):
                        key, value = line.strip().split('=', 1)
                        cls._properties[key.lower()] = value

        for key in cls._properties.keys():
            env_value = os.getenv(key.upper()) or os.getenv(key)
            if env_value is not None:
                cls._properties[key] = env_value

        for arg in sys.argv[1:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                key = key.lstrip('-').lower()
                cls._properties[key] = value

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        if Config._instance is None:
            Config()
        return Config._properties.get(key, default)
