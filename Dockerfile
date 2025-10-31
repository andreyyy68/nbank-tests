FROM python:3.13-slim

# Установка системных зависимостей для Playwright и браузеров
RUN apt-get update && apt-get install -y \
    curl unzip libglib2.0-0 libnss3 libnspr4 libdbus-1-3 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1 libasound2 \
    libatspi2.0-0 libwayland-client0 libxfixes3 libx11-xcb1 \
    python3.13-venv \
    && rm -rf /var/lib/apt/lists/*

# Установка pip и необходимых пакетов
RUN pip install --upgrade pip \
    && pip install pytest pytest-html allure-pytest playwright \
    && playwright install chromium firefox webkit

# Аргументы для сборки (можно задавать при docker build)
ARG TEST_PROFILE=ui
ARG BACKEND_URL=http://localhost:4111
ARG UI_BASE_URL=http://localhost:3000

# ENV переменные по умолчанию
ENV TEST_PROFILE=${TEST_PROFILE}
ENV BACKEND_URL=${BACKEND_URL}
ENV UI_BASE_URL=${UI_BASE_URL}

# Рабочая директория
WORKDIR /app

# Копируем requirements и устанавливаем
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем код тестов
COPY . .

# Запуск от root
USER root

# CMD: ждем доступность UI и запускаем тесты
CMD ["/bin/bash", "-c", "\
    mkdir -p /app/reports /app/logs && \
    echo '>>> Running tests with profile: '$TEST_PROFILE && \
    echo '>>> Backend URL: '$BACKEND_URL && \
    echo '>>> UI URL: '$UI_BASE_URL && \
    until curl -s -f $UI_BASE_URL > /dev/null; do \
        echo 'Waiting for UI...'; sleep 2; \
    done; \
    echo 'UI is up! Starting tests...' && \
    pytest -m \"$TEST_PROFILE\" --html=/app/reports/report.html --self-contained-html --alluredir=/app/reports/allure"]





