"""Celery tasks for Pokémon sync."""
from __future__ import annotations

from flask import current_app
from celery.utils.log import get_task_logger

from app.core.exceptions import PokeApiError, PokemonSyncError
from app.extensions.celery import celery
from app.extensions.database import db
from app.repositories.pokemon import PokemonRepository
from app.services.pokeapi.client import PokeApiClient
from app.services.pokeapi.formatter import PokeAPIFormatter
from app.services.pokemon.service import PokemonService

logger = get_task_logger(__name__)


def _build_service() -> PokemonService:
    client = PokeApiClient(
        base_url=current_app.config["POKEAPI_BASE_URL"],
        timeout=current_app.config["POKEAPI_TIMEOUT"],
    )
    repository = PokemonRepository()
    formatter = PokeAPIFormatter()
    return PokemonService(client, repository, formatter)


def _should_retry(exc: PokemonSyncError, retry_count: int, max_retries: int) -> bool:
    if retry_count >= max_retries:
        return False
    # retry only on upstream failures; validation errors should not retry
    return any("Failed to retrieve" in msg for msg in exc.errors.values())


@celery.task(bind=True, name="pokemon.sync")
def sync_pokemon_task(self, names: list[str]) -> dict:
    """Asynchronously fetch, sanitize, and persist Pokémon records."""

    service = _build_service()
    try:
        result = service.sync(names)
        payload = {
            "synced": [pokemon.name for pokemon in result.synced],
            "synced_ids": [pokemon.id for pokemon in result.synced],
            "errors": result.errors,
        }
        logger.info("Synced %s Pokémon", len(payload["synced"]))
        return payload
    except PokeApiError as exc:
        logger.warning("Retrying sync after upstream error: %s", exc)
        raise self.retry(
            exc=exc,
            countdown=current_app.config.get("CELERY_TASK_RETRY_DELAY", 5),
            max_retries=current_app.config.get("CELERY_TASK_MAX_RETRIES", 3),
        )
    except PokemonSyncError as exc:
        max_retries = current_app.config.get("CELERY_TASK_MAX_RETRIES", 3)
        if _should_retry(exc, self.request.retries, max_retries):
            logger.warning("Retrying sync after transient failure: %s", exc)
            raise self.retry(
                exc=exc,
                countdown=current_app.config.get("CELERY_TASK_RETRY_DELAY", 5),
                max_retries=max_retries,
            )
        logger.error("Sync failed: %s", exc)
        raise
    finally:
        db.session.remove()
