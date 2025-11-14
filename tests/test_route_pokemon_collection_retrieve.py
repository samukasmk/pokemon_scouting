from __future__ import annotations

import responses

API_BASE = "https://pokeapi.co/api/v2/pokemon"


@responses.activate
def test_get_endpoint_collection(client, persisted_pokemon):
    resp = client.get("/api/pokemon/")
    assert resp.status_code == 200

    assert resp.get_json() == [{'abilities': ['static'],
                                'base_experience': 112,
                                'captured_at': '2025-11-14T04:11:17.766955',
                                'height': 4,
                                'id': 1,
                                'name': 'pikachu',
                                'pokedex_id': 25,
                                'sprite': 'http://example.com/sprite.png',
                                'stats': {'speed': 90},
                                'types': ['electric'],
                                'weight': 60}]
