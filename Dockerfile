FROM mcr.microsoft.com/playwright/python:latest

ARG TEST_PROFILE=ui
ARG BACKEND_URL=http://localhost:4111
ARG UI_BASE_URL=http://localhost:3000

ENV TEST_PROFILE=${TEST_PROFILE}
ENV BACKEND_URL=${BACKEND_URL}
ENV UI_BASE_URL=${UI_BASE_URL}

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps
COPY . .

CMD ["/bin/bash", "-c", "\
    mkdir -p /app/reports /app/logs && \
    echo '>>> Running tests with profile: '$TEST_PROFILE && \
    pytest -m \"$TEST_PROFILE\" --html=/app/reports/report.html --self-contained-html --alluredir=/app/reports/allure"]
