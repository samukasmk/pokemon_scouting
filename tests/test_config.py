from __future__ import annotations

from app import create_app


def test_dynaconf_default_environment(monkeypatch):
    monkeypatch.delenv("ENV_FOR_DYNACONF", raising=False)
    app = create_app()
    assert app.config["POKEAPI_TIMEOUT"] == 8
    assert app.config["DEBUG"] is False


def test_dynaconf_development_environment(monkeypatch):
    monkeypatch.setenv("ENV_FOR_DYNACONF", "development")
    app = create_app()
    assert app.config["TESTING"] is False
    assert app.config["SQLALCHEMY_DATABASE_URI"].endswith("pokemon.db")


def test_dynaconf_testing_environment(monkeypatch):
    monkeypatch.setenv("ENV_FOR_DYNACONF", "testing")
    app = create_app()
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
