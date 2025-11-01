FROM python:3.13-slim

ARG TEST_PROFILE=ui
ARG BACKEND_URL=http://localhost:4111
ARG UI_BASE_URL=http://localhost:3000

# ENV переменные по умолчанию
ENV TEST_PROFILE=${TEST_PROFILE}
ENV BACKEND_URL=${BACKEND_URL}
ENV UI_BASE_URL=${UI_BASE_URL}

# Рабочая директория
WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
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





