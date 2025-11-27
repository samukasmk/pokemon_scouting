# Pokémon Scouting App Guide

## Overview
This project delivers an end-to-end Pokémon scouting workflow built with Flask, SQLAlchemy, and PokeAPI. It retrieves, sanitizes, stores, and exports Pokémon data while following security, simplicity, and DSA best practices.

## Available Endpoints
| Method | URI                                     | Description                                             |
| ------ | --------------------------------------- | ------------------------------------------------------- |
| GET    | /api/docs/                              | Swagger UI                                              |
| GET    | /api/pokemon/<name>?refresh=true\|false | Fetch a single Pokémon, optionally forcing a fresh sync |
| GET    | /api/pokemon/                           | List all persisted Pokémons                             |
| POST   | /api/pokemon/                           | Sync Pokémon (body: \`{ "names": [...] }\`)             |
| GET    | /health/                                | Service heartbeat                                       |

- `GET /api/docs/`: Swagger UI

<img src=".docs/images/swagger/main.png" alt="main" width="70%"/>

- `GET /api/pokemon/<name>?refresh=true|false`: Fetch a single Pokémon, optionally forcing a fresh sync

<img src=".docs/images/swagger/retrieve-pokemon.png" alt="retrieve-pokemon" width="70%"/>

- `GET /api/pokemon/`: List all persisted Pokémons
<img src=".docs/images/swagger/retrieve-many-pokemons.png" alt="retrieve-many-pokemons" width="70%"/>

- `POST /api/pokemon/`: Sync Pokémon (body: `{ "names": [...] }`)
<img src=".docs/images/swagger/sync-many-pokemons.png" alt="sync-many-pokemons" width="70%"/>

- `GET /health/`: Service heartbeat

<img src=".docs/images/swagger/health.png" alt="health" width="70%"/>

## Quickstart
1. **Clone the repository**
   ```bash
   git clone https://github.com/samukasmk/pokemon_scouting.git
   cd pokemon_scouting
   ```
2. **Build and start with Docker Compose v2 (uWSGI + Nginx stack)**
   ```bash
   docker compose up --build
   ```
   The stack builds the Flask app image (served via uWSGI), a Celery worker, a RabbitMQ broker, and a lightweight Nginx proxy that exposes everything on `http://localhost`, including Swagger at `/api/docs`.
3. **Shut down the stack**
   ```bash
   docker compose down
   ```

## Local quickstart (without docker)
1. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ``` 
2. **Install Poetry**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Run the web API**
   ```bash
   flask run
   ```

5. **Run Celery worker (requires a broker)**
   ```bash
   # start RabbitMQ locally via compose
   docker compose up rabbitmq -d

   # in another terminal, start the worker
   celery -A celery_worker.celery_app worker --loglevel=info --queues=pokemon_sync
   ```

## Configuration
Environment variables (or the values in `settings.toml`) let you tailor the service:

| Variable | Default | Purpose |
| --- | --- | --- |
| `ENV_FOR_DYNACONF` | `default` | Selects which settings section to load (`default`, `development`, `testing`, `production`) |
| `POKEMON_SQLALCHEMY_DATABASE_URI` | `sqlite:///pokemon.db` | Target database for SQLAlchemy |
| `POKEMON_POKEAPI_BASE_URL` | `https://pokeapi.co/api/v2/pokemon` | Upstream API root |
| `POKEMON_POKEAPI_TIMEOUT` | `8` | HTTP timeout budget in seconds |
| `POKEMON_DEFAULT_POKEMON` | see `settings.toml` | Default list for the CLI sync |
| `POKEMON_CELERY_BROKER_URL` | `amqp://guest:guest@rabbitmq:5672//` | Celery broker URL |
| `POKEMON_CELERY_RESULT_BACKEND` | `rpc://` | Celery result backend |
| `POKEMON_CELERY_TASK_DEFAULT_QUEUE` | `pokemon_sync` | Default Celery queue |
| `POKEMON_CELERY_TASK_TIME_LIMIT` | `30` | Hard time limit for tasks |
| `POKEMON_CELERY_TASK_SOFT_TIME_LIMIT` | `25` | Soft time limit for tasks |
| `POKEMON_CELERY_TASK_RETRY_DELAY` | `5` | Delay between retries |

To scout different Pokémon, either:
- Pass `--names` to the CLI (`flask --app app:create_app pokemon-sync --names eevee snorlax`).
- POST `{"names": ["eevee", "snorlax"]}` to `POST /api/pokemon`.
- Update `DEFAULT_POKEMON` in `settings.toml` (or override via `POKEMON_DEFAULT_POKEMON`) for a new default list.

> For more information about how this config settings pattern works:
> - config management: https://www.dynaconf.com/
> - config file format: https://toml.io/en/

## Testing & Coverage
Run the full suite with enforced 100% coverage:
```bash
pytest
```
Coverage configuration lives in `.coveragerc` and `pyproject.toml`.

## Project Structure
```
app/
  api/          # Flask-Smorest blueprints & schemas
  services/     # PokeAPI client and orchestration services
  repositories/ # Persistence helpers
  core/         # Exceptions and shared plumbing
  models.py     # SQLAlchemy models
  settings.toml # Dynaconf settings (env aware)
wsgi.py         # Production entrypoint
README.md       # This document
AGENTS.md       # A reference for AI agents
```
