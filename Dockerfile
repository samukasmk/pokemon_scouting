# syntax=docker/dockerfile:1.7
FROM python:3.14.0-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="${POETRY_HOME}/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -sf "${POETRY_HOME}/bin/poetry" /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-interaction --no-ansi

COPY . .

RUN groupadd --gid 7777 api \
    && useradd --home /app --gid api --uid 7777 api \
    && chown -R api:api /app

USER api

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]
