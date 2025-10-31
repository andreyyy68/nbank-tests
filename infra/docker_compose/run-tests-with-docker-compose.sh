#!/bin/bash
set -e

# Перейти в директорию скрипта
cd "$(dirname "$0")"

TEST_PROFILE=${1:-"regression"}

# Указываем путь к docker-compose.yml
COMPOSE_FILE="./docker-compose.yml"

# Проверяем, что файл существует
if [ ! -f "$COMPOSE_FILE" ]; then
  echo "❌ Не найден $COMPOSE_FILE"
  exit 1
fi

# Останавливаем старые контейнеры
docker compose -f "$COMPOSE_FILE" down || true

# Запускаем сервисы
docker compose -f "$COMPOSE_FILE" up -d backend frontend nginx

# Запуск тестов
docker compose -f "$COMPOSE_FILE" run --rm tests pytest ${TEST_PROFILE:+-m "$TEST_PROFILE"} \
  --html=/app/reports/report.html --self-contained-html --alluredir=/app/reports/allure \
  -v -s --tb=long --log-level=DEBUG

# Останавливаем контейнеры
docker compose -f "$COMPOSE_FILE" down
