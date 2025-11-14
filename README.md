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
   The stack builds the Flask app image (served via uWSGI) and a lightweight Nginx proxy that exposes everything on `http://localhost:5000`, including Swagger at `/api/docs`.
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

## Configuration
Environment variables (or the values in `app/config.py`) let you tailor the service:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:///instance/pokemon.db` | Target database for SQLAlchemy |
| `POKEAPI_BASE_URL` | `https://pokeapi.co/api/v2/pokemon` | Upstream API root |
| `POKEAPI_TIMEOUT` | `8` | HTTP timeout budget in seconds |
| `FLASK_ENV` | `development` | Controls which config class is used |

To scout different Pokémon, either:
- Pass `--names` to the CLI (`flask --app app:create_app pokemon-sync --names eevee snorlax`).
- POST `{"names": ["eevee", "snorlax"]}` to `POST /api/pokemon`.
- Update `DEFAULT_POKEMON` in `app/config.py` for a new default list.

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
  config.py     # Environment-aware settings
wsgi.py         # Production entrypoint
README.md       # This document
AGENTS.md       # A reference for AI agents
```
