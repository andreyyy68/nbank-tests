#!/bin/bash

IMAGE_NAME=nbank-test
TEST_PROFILE=${1:-"api"}

PROJECT_DIR="$(pwd)"
RAW_REPORTS_DIR="$PROJECT_DIR/test-output/raw"
LOGS_DIR="$PROJECT_DIR/test-output/logs"
ALLURE_RESULTS_DIR="$PROJECT_DIR/test-output/allure-results"


mkdir -p "$RAW_REPORTS_DIR" "$LOGS_DIR" "$ALLURE_RESULTS_DIR"

echo ">>> Сборка Docker образа: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

echo ">>> Запуск тестов профиля: $TEST_PROFILE"

docker run --rm \
  --network nbank-network \
  -v "$RAW_REPORTS_DIR":/app/test-output/raw \
  -v "$LOGS_DIR":/app/test-output/logs \
  -v "$ALLURE_RESULTS_DIR":/app/test-output/allure-results \
  -e TEST_PROFILE="$TEST_PROFILE" \
  -e BACKEND_URL="http://backend:4111/api/v1" \
  -e UI_BASE_URL="http://frontend:80" \
  $IMAGE_NAME \
  bash -c "\
    pytest --alluredir=/app/test-output/allure-results \
           --junitxml=/app/test-output/raw/results.xml \
           --tb=short
  "

echo ">>> Тесты завершены"
