"""Helpers for dealing with Pokémon naming quirks."""
from __future__ import annotations

ALIASES = {
    "terodactyl": "aerodactyl",
}


def normalize_name(name: str) -> str:
    normalized = name.strip().lower()
    return ALIASES.get(normalized, normalized)
