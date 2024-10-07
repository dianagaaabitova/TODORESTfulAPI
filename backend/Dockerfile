FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_HOME="/etc/poetry" \
    POETRY_CACHE_DIR="/tmp/poetry_cache" \
    POETRY_VERSION=1.7.0

ENV ALEMBIC_CONFIG=alembic.ini

WORKDIR /usr/src/todo/backend/app
COPY ./app .

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN poetry install
