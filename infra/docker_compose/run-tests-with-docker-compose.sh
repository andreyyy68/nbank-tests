#!/bin/bash
set -e

# Профиль тестов (ui, api или оба), по умолчанию "ui or api"
TEST_PROFILE=${1:-"ui or api"}

# Очищаем старые контейнеры, тома и сирот
echo ">>> Stopping and removing old containers..."
docker compose down --volumes --remove-orphans

# Поднимаем backend и frontend
echo ">>> Starting backend and frontend..."
docker compose up -d backend frontend

# Ждем 5 секунд (можно увеличить, если сервисы тяжелые)
sleep 5

# Запуск тестов через твой образ
echo ">>> Running tests in Docker container..."
docker run --rm \
  -e TEST_PROFILE="$TEST_PROFILE" \
  -e BACKEND_URL="http://host.docker.internal:4111" \
  -e UI_BASE_URL="http://host.docker.internal:3000" \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/logs:/app/logs \
  your-image-name

echo ">>> Tests finished!"
