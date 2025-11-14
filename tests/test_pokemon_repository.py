from __future__ import annotations

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import RepositoryError
from app.repositories.pokemon import PokemonRepository


def sample_payload_factory(sample_payload):
    return {
        "pokedex_id": sample_payload["id"],
        "name": sample_payload["name"],
        "base_experience": sample_payload["base_experience"],
        "height": sample_payload["height"],
        "weight": sample_payload["weight"],
        "abilities": ["static"],
        "types": ["electric"],
        "stats": {"attack": 55},
        "sprite": "http://example.com/sprite.png",
    }


def test_upsert_and_list(sample_payload):
    repo = PokemonRepository()
    payload = sample_payload_factory(sample_payload)
    repo.upsert(payload)
    payload["base_experience"] = 130
    repo.upsert(payload)
    records = repo.list_all()
    assert len(records) == 1
    assert records[0].base_experience == 130


def test_upsert_handles_commit_failure(sample_payload, monkeypatch):
    repo = PokemonRepository()
    payload = sample_payload_factory(sample_payload)

    class BrokenSession:
        def __init__(self, session):
            self._session = session

        def add(self, obj):
            return self._session.add(obj)

        def commit(self):
            raise SQLAlchemyError("boom")

        def rollback(self):
            return self._session.rollback()

    repo.session = BrokenSession(repo.session)
    with pytest.raises(RepositoryError):
        repo.upsert(payload)


def test_delete_all_returns_count(persisted_pokemon):
    repo = PokemonRepository()
    assert repo.delete_all() == 1


def test_delete_all_handles_failure(monkeypatch):
    repo = PokemonRepository()

    class BrokenSession:
        def __init__(self, session):
            self._session = session

        def commit(self):
            raise SQLAlchemyError("boom")

        def rollback(self):
            return self._session.rollback()

    repo.session = BrokenSession(repo.session)
    with pytest.raises(RepositoryError):
        repo.delete_all()
