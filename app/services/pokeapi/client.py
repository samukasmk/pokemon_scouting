"""Client for retrieving data from PokeAPI."""
from __future__ import annotations

from typing import Any

import requests
from requests import Session

from app.core.exceptions import PokeApiError
from app.utils.naming import normalize_name


class PokeApiClient:
    """Thin wrapper around requests to interact with PokeAPI."""

    def __init__(self, base_url: str, timeout: int = 8, session: Session | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def fetch_pokemon(self, name: str) -> dict[str, Any]:
        if not name:
            raise PokeApiError("Pokémon name cannot be empty")

        name = normalize_name(name)
        url = f"{self.base_url}/{name}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise PokeApiError(f"Failed to retrieve Pokémon '{name}': {exc}") from exc
        if "id" not in data:
            raise PokeApiError(f"PokeAPI payload for '{name}' is missing the id field")
        return data
