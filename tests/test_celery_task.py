from __future__ import annotations

import pytest
import responses
from celery.exceptions import Retry
from flask import current_app

from app.core.exceptions import PokeApiError, PokemonSyncError
from app.tasks import pokemon as pokemon_tasks
from app.tasks.pokemon import _should_retry, sync_pokemon_task

API_BASE = "https://pokeapi.co/api/v2/pokemon"


@responses.activate
def test_sync_pokemon_task_success(sample_payload):
    responses.add(
        responses.GET,
        f"{API_BASE}/{sample_payload['name']}",
        json=sample_payload,
        status=200,
    )

    eager_result = sync_pokemon_task.apply(args=([sample_payload["name"]],), throw=True)
    assert eager_result.successful()
    body = eager_result.get()
    assert body["synced"] == [sample_payload["name"]]
    assert body["errors"] == {}


def test_should_retry_only_on_upstream_failures():
    exc = PokemonSyncError("boom", errors={"pikachu": "Failed to retrieve Pokémon 'pikachu': timeout"})
    assert _should_retry(exc, 0, 3)
    assert not _should_retry(exc, 3, 3)

    non_retryable = PokemonSyncError("boom", errors={"pikachu": "not found"})
    assert not _should_retry(non_retryable, 0, 3)


def test_sync_pokemon_task_raises_on_invalid_names():
    with pytest.raises(PokemonSyncError):
        sync_pokemon_task.apply(args=([],), throw=True)


def test_sync_pokemon_task_retries_on_upstream_error(monkeypatch):
    class StubService:
        def sync(self, names):  # pragma: no cover - behavior asserted via retry
            raise PokeApiError("Failed to retrieve Pokémon 'pikachu': timeout")

    monkeypatch.setattr(pokemon_tasks, "_build_service", lambda: StubService())
    with pytest.raises(Retry):
        sync_pokemon_task.apply(args=(['pikachu'],), throw=True)


def test_sync_pokemon_task_retries_on_transient_sync_error(monkeypatch):
    transient = PokemonSyncError(
        "Unable to sync requested Pokémon",
        errors={"pikachu": "Failed to retrieve Pokémon 'pikachu': timeout"},
    )

    class StubService:
        def sync(self, names):  # pragma: no cover - behavior asserted via retry
            raise transient

    monkeypatch.setattr(pokemon_tasks, "_build_service", lambda: StubService())
    with pytest.raises(Retry):
        sync_pokemon_task.apply(args=(['pikachu'],), throw=True)


def test_celery_context_binds_flask_app(app):
    celery_app = app.extensions["celery"]

    @celery_app.task
    def capture_app_name():
        return current_app.name

    eager_result = capture_app_name.apply(throw=True)
    assert eager_result.get() == app.name
