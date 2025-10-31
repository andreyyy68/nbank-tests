#! /bin/bash

# Настройка
IMAGE_NAME=nbank-test
TEST_PROFILE=${1:-api}
TIMESTAMP=$(date +"%Y%m%d_%H%M")
TEST_OUTPUT_DIR="$(pwd)/test-output/$TIMESTAMP"

# Собираем докер образ
echo ">>> Сборка тестов запущена"
docker build -t $IMAGE_NAME .

mkdir -p "$TEST_OUTPUT_DIR/logs"
mkdir -p "$TEST_OUTPUT_DIR/reports"

echo ">>> Тесты запущены"

docker run --rm \
  -v "$TEST_OUTPUT_DIR/logs":/app/logs \
  -v "$TEST_OUTPUT_DIR/reports":/app/reports \
  -e TEST_PROFILE="$TEST_PROFILE" \
  -e BACKEND_URL="http://localhost:4111/api/v1" \
  -e UI_BASE_URL="http://localhost:3000" \
  $IMAGE_NAME

echo ">>> Тесты завершены"