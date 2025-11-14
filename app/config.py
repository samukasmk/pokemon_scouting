"""Application configuration and settings helpers."""
from __future__ import annotations

import os
from typing import Type


def _default_database_uri() -> str:
    instance_path = os.getenv("INSTANCE_PATH", os.path.join(os.getcwd(), "instance"))
    os.makedirs(instance_path, exist_ok=True)
    return f"sqlite:///{os.path.join(instance_path, 'pokemon.db')}"


class BaseConfig:
    """Base configuration shared across environments."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", _default_database_uri())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # API settings
    API_TITLE = "Pokémon Scouting API"
    API_VERSION = "1.0.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # PokeAPI settings
    POKEAPI_BASE_URL = os.getenv("POKEAPI_BASE_URL", "https://pokeapi.co/api/v2/pokemon")
    POKEAPI_TIMEOUT = int(os.getenv("POKEAPI_TIMEOUT", "8"))
    DEFAULT_POKEMON = (
        "pikachu",
        "dhelmise",
        "charizard",
        "parasect",
        "terodactyl",
        "kingler",
    )


class TestingConfig(BaseConfig):
    """Configuration used during automated tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


CONFIG_MAP: dict[str, Type[BaseConfig]] = {
    "default": BaseConfig,
    "testing": TestingConfig,
}


def get_config(name: str | None = None) -> Type[BaseConfig]:
    """Return a configuration class for the supplied name."""
    if not name:
        return BaseConfig
    return CONFIG_MAP.get(name.lower(), BaseConfig)
