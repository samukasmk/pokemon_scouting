# syntax=docker/dockerfile:1.7
FROM python:3.14.0-slim

# install app dependencies
RUN apt update && apt upgrade -y && apt install --no-install-recommends -y curl

# define poetry env settings
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTCODE=1 \
	PIP_NO_CACHE_DIR=off \
	PIP_DEFAULT_TIMEOUT=100 \
	POETRY_VERSION=2.1.2 \
	POETRY_HOME="/opt/poetry" \
	POETRY_VIRTUALENVS_CREATE=false
ENV	PATH="$PATH:$POETRY_HOME/bin"

# update pip tool
RUN pip install -U pip

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# create user and group
RUN groupadd --gid 7777 api && useradd --gid api --uid 7777 api --create-home --no-user-group

# set app directory
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN chown -R api:api /app

# install dependencies
RUN poetry install

# define app user privileges
USER api

# export fastapi port
EXPOSE 5000

# define fastapi command
CMD ["flask", "--app", "app:create_app", "run", "--host=0.0.0.0", "--port=5000"]
