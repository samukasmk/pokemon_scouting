from __future__ import annotations

import responses

API_BASE = "https://pokeapi.co/api/v2/pokemon"


@responses.activate
def test_retrieve_pokemon_resource(client, sample_payload):
    pikachu_payload = dict(sample_payload)
    aerodactyl_payload = dict(sample_payload)
    aerodactyl_payload["id"] = 142
    aerodactyl_payload["name"] = "aerodactyl"
    responses.add(responses.GET, f"{API_BASE}/pikachu", json=pikachu_payload, status=200)
    responses.add(
        responses.GET, f"{API_BASE}/aerodactyl", json=aerodactyl_payload, status=200
    )

    resp = client.get("/api/pokemon/pikachu")
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'pikachu'

    resp = client.get("/api/pokemon/aerodactyl")
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'aerodactyl'


@responses.activate
def test_get_pokemon_refresh_fetches_when_missing(client, sample_payload):
    responses.add(
        responses.GET,
        f"{API_BASE}/pikachu",
        json=sample_payload,
        status=200,
    )
    resp = client.get("/api/pokemon/pikachu?refresh=true")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "pikachu"


def test_get_pokemon_uses_cached_record(client, persisted_pokemon):
    resp = client.get("/api/pokemon/pikachu")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == persisted_pokemon.id


@responses.activate
def test_get_pokemon_handles_sync_failure(client):
    responses.add(
        responses.GET,
        f"{API_BASE}/missingno",
        status=404,
    )

    resp = client.get("/api/pokemon/missingno?refresh=true")
    assert resp.status_code == 404
    body = resp.get_json()
    assert "errors" in body
