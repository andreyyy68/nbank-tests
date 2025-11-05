#!/bin/bash

# Создаём папки
mkdir -p test-output/raw
mkdir -p test-output/html

# Прогон тестов
pytest --alluredir=test-output/raw

# Генерация HTML
allure generate test-output/raw --clean -o test-output/html

# Открытие отчёта
allure open test-output/html