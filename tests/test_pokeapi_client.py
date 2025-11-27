from __future__ import annotations

import pytest
import responses

from app.core.exceptions import PokeApiError
from app.services.pokeapi.client import PokeApiClient


@responses.activate
def test_fetch_pokemon_success(sample_payload):
    client = PokeApiClient("https://pokeapi.co/api/v2/pokemon", timeout=1)
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/pikachu",
        json=sample_payload,
        status=200,
    )
    data = client.fetch_pokemon(" Pikachu ")
    assert data["id"] == sample_payload["id"]


@responses.activate
def test_fetch_pokemon_error_status():
    client = PokeApiClient("https://pokeapi.co/api/v2/pokemon")
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/missingno",
        status=404,
    )
    with pytest.raises(PokeApiError):
        client.fetch_pokemon("missingno")


def test_fetch_pokemon_rejects_blank_name():
    client = PokeApiClient("https://pokeapi.co/api/v2/pokemon")
    with pytest.raises(PokeApiError):
        client.fetch_pokemon("   ")


def test_fetch_pokemon_rejects_empty_name():
    client = PokeApiClient("https://pokeapi.co/api/v2/pokemon")
    with pytest.raises(PokeApiError):
        client.fetch_pokemon("")


@responses.activate
def test_fetch_pokemon_requires_id(sample_payload):
    client = PokeApiClient("https://pokeapi.co/api/v2/pokemon")
    bad_payload = dict(sample_payload)
    bad_payload.pop("id")
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/pikachu",
        json=bad_payload,
        status=200,
    )
    with pytest.raises(PokeApiError):
        client.fetch_pokemon("pikachu")
