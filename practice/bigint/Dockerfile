# Запуск тестов домашки в Docker (poetry внутри образа):
#   make docker-test   или   docker compose run --rm test
FROM python:3.12-slim

ENV POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.8.5 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir poetry==${POETRY_VERSION} \
 && poetry install --no-interaction --no-ansi

CMD ["python", "-m", "pytest", "-v"]