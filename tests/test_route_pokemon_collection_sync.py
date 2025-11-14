from __future__ import annotations

import responses

API_BASE = "https://pokeapi.co/api/v2/pokemon"


@responses.activate
def test_sync_and_retrieve_flow(client, sample_payload):
    pikachu_payload = dict(sample_payload)
    aerodactyl_payload = dict(sample_payload)
    aerodactyl_payload["id"] = 142
    aerodactyl_payload["name"] = "aerodactyl"
    responses.add(responses.GET, f"{API_BASE}/pikachu", json=pikachu_payload, status=200)
    responses.add(
        responses.GET, f"{API_BASE}/aerodactyl", json=aerodactyl_payload, status=200
    )

    resp = client.post(
        "/api/pokemon/",
        json={"names": ["Pikachu", "Terodactyl"]},
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert len(body["synced"]) == 2

    resp = client.get("/api/pokemon/")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


@responses.activate
def test_sync_endpoint_validation(client):
    resp = client.post("/api/pokemon/", json={"names": []})
    assert resp.status_code == 422


@responses.activate
def test_sync_handles_upstream_error(client):
    responses.add(
        responses.GET,
        f"{API_BASE}/pikachu",
        status=404,
    )
    resp = client.post("/api/pokemon/", json={"names": ["pikachu"]})
    assert resp.status_code == 400
    body = resp.get_json()
    assert "errors" in body
