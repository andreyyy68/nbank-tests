#!/bin/bash

TEST_PROFILE=${1:-"regression"}

# Папка для отчетов на хосте
REPORTS_DIR="$(pwd)/test-output"
mkdir -p "$REPORTS_DIR"

# Останавливаем старые контейнеры (без ошибки, если нет)
docker-compose down || true

# Поднимаем сервисы
docker-compose up -d backend frontend nginx

sleep 10

# Запуск тестов с отчетами
docker-compose run --rm \
  -v "$REPORTS_DIR":/app/reports \
  tests pytest -m "$TEST_PROFILE" \
    --html=/app/reports/report.html \
    --self-contained-html \
    --alluredir=/app/reports/allure \
    -v -s --tb=long --log-level=DEBUG

# Завершаем окружение
docker-compose down
