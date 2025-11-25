"""Service orchestrating Pokémon sync operations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.core.exceptions import PokemonSyncError
from app.models import Pokemon
from app.repositories.pokemon import PokemonRepository
from app.services.pokeapi.formatter import PokeAPIFormatter
from app.services.pokeapi.client import PokeApiClient
from app.utils.naming import normalize_name


@dataclass(slots=True)
class SyncResult:
    synced: list[Pokemon]
    errors: dict[str, str]

    @property
    def success(self) -> bool:
        return bool(self.synced) and not self.errors


class PokemonService:
    """Coordinates PokeAPI retrievals, sanitization, and persistence."""

    def __init__(self, client: PokeApiClient, repository: PokemonRepository, formatter: PokeAPIFormatter):
        self.client = client
        self.repository = repository
        self.formatter = formatter

    def sync(self, names: Iterable[str]) -> SyncResult:
        """Fetch, sanitize, and persist multiple Pokémon."""

        # get unique names normalized but keeping the sort positions
        unique_names = []
        seen = set()
        for name in names:
            normalized = normalize_name(name)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            unique_names.append(normalized)

        # raise error if has no names to sync
        if not unique_names:
            raise PokemonSyncError("No valid Pokémon names provided")

        synced_records: list[Pokemon] = []
        errors: dict[str, str] = {}

        # get each Pokémon and create or update in db
        for name in unique_names:
            try:
                raw = self.client.fetch_pokemon(name)
                sanitized = self.formatter.build(raw)
                saved = self.repository.upsert(sanitized)
                synced_records.append(saved)
            except Exception as exc:
                errors[name] = str(exc)

        # raise error if has no synced records
        if not synced_records:
            raise PokemonSyncError("Unable to sync requested Pokémon", errors=errors)

        return SyncResult(synced=synced_records, errors=errors)
