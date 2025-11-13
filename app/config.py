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
