import os
import configparser
from pathlib import Path
from typing import List, Dict, Type, Optional

# Разделяем: ключ - поле из request, значение - поле из response (2)
class ComparisonRule:
    def __init__(self, response_class_name: str, field_pairs: List[str]):
        self._response_class_name = response_class_name
        self.field_pairs = field_pairs
        self._field_mapping: Dict[str, str] = {}

        for pair in field_pairs:
            parts = pair.split('=')
            if len(parts) == 2:
                self._field_mapping[parts[0].strip()] = parts[1].strip()
            else:
                self._field_mapping[pair.strip()] = pair.strip()

    @property
    def response_class_name(self) -> str:
        return self._response_class_name

    @property
    def field_mapping(self) -> Dict[str, str]:
        return self._field_mapping.copy()

# Отсюда начинаем (1)
class ModelComparisonConfigLoader:
    def __init__(self, config_file: str):
        self.rules: Dict[str, ComparisonRule] = {}
        self._load_config(config_file)

    def _load_config(self, config_file: str):
        path = Path(__file__).parents[5] / 'resources' / f'{config_file}' # config_file - model_comparison.properties / передаем название файла

        if not os.path.exists(path):
            raise FileNotFoundError(f'Config file not found: {config_file}')

        config = configparser.ConfigParser() # Получаем объект кофинга
        config.optionxform = str
        config.read(path) # Открываем файл на чтение

        for key in config.defaults(): # Итерируемся  key - CreateUserRequest
            value = config.defaults()[key] # "UserResponse: username=userName, password=password..."
            target = value.split(':') #"UserResponse", "username=userName, password=password..." Убрали двоеточие
            if len(target) != 2:
                continue

            response_class = target[0].strip() #UserResponse
            field_list = [field.strip() for field in target[1].split(',')] # "username=userName", "password=password"..

            self.rules[key.strip()] = ComparisonRule(response_class, field_list) #ComparisonRule(response_class, field_list)

    def get_rule_for(self, request_class: Type) -> Optional[ComparisonRule]: # CreateUserRequest
        return self.rules.get(request_class.__name__)