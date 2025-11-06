#!/bin/bash

IMAGE_NAME=nbank-test
TEST_PROFILE=${1:-"api"}

PROJECT_DIR="$(pwd)"
RAW_REPORTS_DIR="$PROJECT_DIR/test-output/raw"
LOGS_DIR="$PROJECT_DIR/test-output/logs"

mkdir -p "$RAW_REPORTS_DIR" "$LOGS_DIR"

echo ">>> Сборка Docker образа: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

echo ">>> Запуск тестов профиля: $TEST_PROFILE"

docker run --rm \
  --network nbank-network \
  -v "$RAW_REPORTS_DIR":/app/reports/raw \
  -v "$LOGS_DIR":/app/logs \
  -e TEST_PROFILE="$TEST_PROFILE" \
  -e BACKEND_URL="http://backend:4111/api/v1" \
  -e UI_BASE_URL="http://frontend:80" \
  $IMAGE_NAME \
  bash -c "\
    pytest --alluredir=/app/test-output/allure-results \
       --junitxml=/app/reports/raw/results.xml \
       --tb=short
  "

echo ">>> Тесты завершены. Результаты в $RAW_REPORTS_DIR"