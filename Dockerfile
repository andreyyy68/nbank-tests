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
    echo '>>> Starting tests immediately...' && \
    pytest -m \"$TEST_PROFILE\" --html=/app/reports/report.html --self-contained-html --alluredir=/app/reports/allure"]





