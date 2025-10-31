#!/bin/bash

TEST_PROFILE=${1:-"ui or api"}

# Останавливаем старые контейнеры
docker compose down

# Запускаем сервисы
docker compose up -d backend frontend nginx

# Запуск тестов
docker compose run --rm tests pytest ${TEST_PROFILE:+-m "$TEST_PROFILE"} \
    --html=/app/reports/report.html --self-contained-html --alluredir=/app/reports/allure \
    -v -s --tb=long --log-level=DEBUG

# Останавливаем контейнеры
docker compose down
