from __future__ import annotations

import pytest

from app.core.exceptions import PokemonSyncError
from app.repositories.pokemon import PokemonRepository
from app.services.pokeapi.formatter import PokeAPIFormatter
from app.services.pokemon.service import PokemonService


class DummyClient:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def fetch_pokemon(self, name):
        self.calls.append(name)
        if name == "missingno":
            raise ValueError("boom")
        data = dict(self.payload)
        data["name"] = name
        data["id"] += len(self.calls)
        return data


def make_service(sample_payload):
    repo = PokemonRepository()
    client = DummyClient(sample_payload)
    formatter = PokeAPIFormatter()
    return PokemonService(client, repo, formatter), client


def test_sync_deduplicates_and_alias(sample_payload):
    service, client = make_service(sample_payload)
    result = service.sync(["Pikachu", "pikachu", "Terodactyl"])
    assert len(result.synced) == 2
    assert "aerodactyl" in {rec.name for rec in result.synced}
    assert client.calls[1] == "aerodactyl"
    assert result.success is True


def test_sync_raises_when_all_fail(sample_payload):
    service, client = make_service(sample_payload)
    client.payload["id"] = 100
    with pytest.raises(PokemonSyncError):
        service.sync(["missingno"])


def test_sync_without_valid_names_raises(sample_payload):
    service, _ = make_service(sample_payload)
    with pytest.raises(PokemonSyncError):
        service.sync(["   "])
