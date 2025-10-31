#! /bin/bash

echo ">>> Остановить docker-compose"
docker compose down

echo ">>> Запуск docker-compose"
docker compose up -d

echo ">>> Проверяем логи"
