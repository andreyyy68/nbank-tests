#!/bin/bash

IMAGE_NAME=nbank-test
PROJECT_DIR="$(pwd)"
RAW_REPORTS_DIR="$PROJECT_DIR/test-output/raw"
LOGS_DIR="$PROJECT_DIR/test-output/logs"

mkdir -p "$RAW_REPORTS_DIR" "$LOGS_DIR"

echo ">>> Сборка Docker образа: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# --- Запуск UI тестов ---
echo ">>> Запуск UI тестов"
docker run --rm \
  --network nbank-network \
  -v "$RAW_REPORTS_DIR":/app/reports/raw \
  -v "$LOGS_DIR":/app/logs \
  -e TEST_PROFILE="ui" \
  -e BACKEND_URL="http://backend:4111/api/v1" \
  -e UI_BASE_URL="http://frontend:80" \
  $IMAGE_NAME \
  bash -c "pytest src/main/ui/tests --junitxml=/app/reports/raw/ui_results.xml --tb=short"

# --- Запуск API тестов ---
echo ">>> Запуск API тестов"
docker run --rm \
  --network nbank-network \
  -v "$RAW_REPORTS_DIR":/app/reports/raw \
  -v "$LOGS_DIR":/app/logs \
  -e TEST_PROFILE="api" \
  -e BACKEND_URL="http://backend:4111/api/v1" \
  $IMAGE_NAME \
  bash -c "pytest src/main/api/tests --junitxml=/app/reports/raw/api_results.xml --tb=short"

echo ">>> Тесты завершены. Результаты в $RAW_REPORTS_DIR"
