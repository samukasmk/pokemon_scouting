from __future__ import annotations

import json
from pathlib import Path

import pytest
from flask import Flask
from marshmallow import ValidationError

from app import create_app
from app.core.exceptions import PokemonSyncError
from app.extensions import db as _db
from app.models import Pokemon


@pytest.fixture(scope="session")
def app() -> Flask:
    app = create_app("testing")
    yield app


@pytest.fixture(autouse=True)
def app_context(app):
    ctx = app.app_context()
    ctx.push()
    _db.create_all()
    yield
    _db.session.remove()
    _db.drop_all()
    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_payload() -> dict:
    path = Path(__file__).with_name("sample_pokemon.json")
    return json.loads(path.read_text())


@pytest.fixture
def persisted_pokemon(sample_payload) -> Pokemon:
    pokemon = Pokemon(
        pokedex_id=sample_payload["id"],
        name=sample_payload["name"],
        base_experience=sample_payload["base_experience"],
        height=sample_payload["height"],
        weight=sample_payload["weight"],
        abilities=["static"],
        types=["electric"],
        stats={"speed": 90},
        sprite="http://example.com/sprite.png",
    )
    _db.session.add(pokemon)
    _db.session.commit()
    return pokemon
