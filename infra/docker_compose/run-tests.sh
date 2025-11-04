#! /bin/bash

IMAGE_NAME=nbank-test
TEST_PROFILE=${1:-"api"}  # api или ui
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TEST_OUTPUT_DIR="$(pwd)/test-output/$TIMESTAMP"
RAW_REPORTS_DIR="$TEST_OUTPUT_DIR/reports/raw"
ALLURE_HTML_DIR="$TEST_OUTPUT_DIR/reports/html"
LOGS_DIR="$TEST_OUTPUT_DIR/logs"

# ==========================
# Создаём папки для результатов
# ==========================
mkdir -p "$RAW_REPORTS_DIR"
mkdir -p "$ALLURE_HTML_DIR"
mkdir -p "$LOGS_DIR"

# ==========================
# Сборка Docker образа
# ==========================
echo ">>> Сборка Docker образа: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# ==========================
# Запуск тестов в Docker с генерацией raw Allure результатов
# ==========================
echo ">>> Запуск тестов профиля: $TEST_PROFILE"

docker run --rm \
  --network nbank-network \
  -v "$RAW_REPORTS_DIR":/app/reports/raw \
  -v "$ALLURE_HTML_DIR":/app/reports/html \
  -v "$LOGS_DIR":/app/logs \
  -e TEST_PROFILE="$TEST_PROFILE" \
  -e BACKEND_URL="http://backend:4111/api/v1" \
  -e UI_BASE_URL="http://frontend:80" \
  $IMAGE_NAME \
  bash -c "\
    pytest --alluredir=/app/reports/raw && \
    allure generate /app/reports/raw --clean -o /app/reports/html \
  "


echo ">>> Запуск тестов профиля: $TEST_PROFILE"