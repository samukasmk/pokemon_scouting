from __future__ import annotations

from app.services.pokeapi.formatter import PokeAPIFormatter


def test_formatter_build(sample_payload):
    sanitized = PokeAPIFormatter.build(sample_payload)
    assert sanitized["name"] == "pikachu"
    assert sanitized["abilities"] == ["static"]
    assert sanitized["types"] == ["electric"]
    assert sanitized["stats"]["speed"] == 90
