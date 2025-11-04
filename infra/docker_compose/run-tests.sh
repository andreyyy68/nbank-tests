#! /bin/bash

IMAGE_NAME=nbank-test
TEST_PROFILE=${1:-"api"}  # api или ui

# Папка для отчётов (фиксированная)
TEST_OUTPUT_DIR="$(pwd)/test-output"
RAW_REPORTS_DIR="$TEST_OUTPUT_DIR/raw"
ALLURE_HTML_DIR="$TEST_OUTPUT_DIR/html"
LOGS_DIR="$TEST_OUTPUT_DIR/logs"

# ==========================
# Создаём папки для результатов
# ==========================
mkdir -p "$RAW_REPORTS_DIR" "$ALLURE_HTML_DIR" "$LOGS_DIR"

# ==========================
# Сборка Docker образа
# ==========================
echo ">>> Сборка Docker образа: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# ==========================
# Запуск тестов в Docker с генерацией Allure отчётов
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

echo ">>> Тесты завершены. HTML отчёт доступен в $ALLURE_HTML_DIR"
