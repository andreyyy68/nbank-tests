#!/bin/bash

echo ">>> Проверяем, что backend и frontend запущены"
docker ps

echo ">>> Запускаем pytest"
pytest -m "api or ui" -v --alluredir=reports