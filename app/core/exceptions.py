"""Custom exception hierarchy for the Pokemon scouting app."""
from __future__ import annotations


class AppError(Exception):
    """Base application error."""


class PokeApiError(AppError):
    """Raised when the upstream PokeAPI call fails."""


class RepositoryError(AppError):
    """Raised when persistence operations fail."""


class PokemonSyncError(AppError):
    """Raised when the sync pipeline cannot complete."""

    def __init__(self, message: str, errors: dict[str, str] | None = None):
        super().__init__(message)
        self.errors = errors or {}
