"""Data sanitization helpers for Pokémon payloads."""
from __future__ import annotations

from typing import Any


class PokeAPIFormatter:
    """Transforms raw PokeAPI payloads into persistable dictionaries."""

    @staticmethod
    def build(payload: dict[str, Any]) -> dict[str, Any]:
        abilities = sorted(
            {entry["ability"]["name"] for entry in payload.get("abilities", [])}
        )
        types = sorted({entry["type"]["name"] for entry in payload.get("types", [])})
        stats = {
            stat_entry["stat"]["name"]: stat_entry["base_stat"]
            for stat_entry in payload.get("stats", [])
        }
        return {
            "pokedex_id": payload["id"],
            "name": payload["name"].lower(),
            "base_experience": payload.get("base_experience", 0),
            "height": payload.get("height", 0),
            "weight": payload.get("weight", 0),
            "abilities": abilities,
            "types": types,
            "stats": stats,
            "sprite": payload.get("sprites", {}).get("front_default"),
        }
