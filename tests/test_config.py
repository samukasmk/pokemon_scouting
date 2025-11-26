from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

from app import create_app
from app.extensions.database import db as _db


@contextmanager
def build_local_app(env: str | None = None):
    """Create an app for config checks and ensure database resources are closed."""
    app = create_app(env)
    try:
        yield app
    finally:
        with app.app_context():
            _db.session.remove()
            _db.drop_all()
            _db.engine.dispose()

        db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        if db_uri.startswith("sqlite:///") and not db_uri.endswith(":memory:"):
            db_path = Path(db_uri.replace("sqlite:///", ""))
            db_path.unlink(missing_ok=True)


def test_dynaconf_default_environment(monkeypatch):
    monkeypatch.delenv("ENV_FOR_DYNACONF", raising=False)
    with build_local_app() as app:
        assert app.config["POKEAPI_TIMEOUT"] == 8
        assert app.config["DEBUG"] is False


def test_dynaconf_development_environment_by_env_var(monkeypatch):
    monkeypatch.setenv("ENV_FOR_DYNACONF", "development")
    with build_local_app() as app:
        assert app.config["TESTING"] is False
        assert app.config["SQLALCHEMY_DATABASE_URI"].endswith("pokemon.db")


def test_dynaconf_development_environment_by_env_name(monkeypatch):
    with build_local_app("development") as app:
        assert app.config["TESTING"] is False
        assert app.config["SQLALCHEMY_DATABASE_URI"].endswith("pokemon.db")


def test_dynaconf_testing_environment_by_env_var(monkeypatch):
    monkeypatch.setenv("ENV_FOR_DYNACONF", "testing")
    with build_local_app() as app:
        assert app.config["TESTING"] is True
        assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_dynaconf_testing_environment_by_env_name(monkeypatch):
    with build_local_app("testing") as app:
        assert app.config["TESTING"] is True
        assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
