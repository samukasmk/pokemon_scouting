from __future__ import annotations

import responses

from app.core.exceptions import PokemonSyncError
from app.tasks.pokemon import sync_pokemon_task

API_BASE = "https://pokeapi.co/api/v2/pokemon"


@responses.activate
def test_async_sync_flow(client, sample_payload):
    responses.add(
        responses.GET,
        f"{API_BASE}/{sample_payload['name']}",
        json=sample_payload,
        status=200,
    )

    resp = client.post("/api/pokemon/async", json={"names": [sample_payload["name"]]})
    assert resp.status_code == 202
    task_id = resp.get_json()["task_id"]

    status_resp = client.get(f"/api/pokemon/tasks/{task_id}")
    assert status_resp.status_code == 200
    body = status_resp.get_json()
    assert body["task_id"] == task_id
    assert body["state"] in {"SUCCESS", "PENDING"}
    if body["result"]:
        assert sample_payload["name"] in body["result"]["synced"]


def test_task_status_success_branch(client, monkeypatch):
    class DummyResult:
        state = "SUCCESS"
        result = {"synced": ["pikachu"], "synced_ids": [1], "errors": {}}

        def successful(self):
            return True

        def failed(self):
            return False

    celery_app = client.application.extensions["celery"]
    monkeypatch.setattr(celery_app, "AsyncResult", lambda _: DummyResult())

    status_resp = client.get("/api/pokemon/tasks/dummy-success")
    assert status_resp.status_code == 200
    body = status_resp.get_json()
    assert body["state"] == "SUCCESS"
    assert body["result"]["synced"] == ["pikachu"]


def test_task_status_failure_branch(client, monkeypatch):
    class DummyResult:
        state = "FAILURE"
        result = ValueError("boom")

        def successful(self):
            return False

        def failed(self):
            return True

    celery_app = client.application.extensions["celery"]
    monkeypatch.setattr(celery_app, "AsyncResult", lambda _: DummyResult())

    status_resp = client.get("/api/pokemon/tasks/dummy")
    assert status_resp.status_code == 200
    body = status_resp.get_json()
    assert body["state"] == "FAILURE"
    assert body["result"]["errors"] == {"task": "boom"}


def test_task_status_failure_with_app_error(client, monkeypatch):
    class DummyResult:
        state = "FAILURE"
        result = PokemonSyncError("boom", errors={"pikachu": "timeout"})

        def successful(self):
            return False

        def failed(self):
            return True

    celery_app = client.application.extensions["celery"]
    monkeypatch.setattr(celery_app, "AsyncResult", lambda _: DummyResult())

    status_resp = client.get("/api/pokemon/tasks/dummy-app-error")
    assert status_resp.status_code == 200
    body = status_resp.get_json()
    assert body["state"] == "FAILURE"
    assert body["result"]["errors"] == {"pikachu": "timeout"}
