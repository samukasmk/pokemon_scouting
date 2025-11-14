"""API blueprint exposing Pokémon resources."""
from __future__ import annotations

from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint
from app.api.schemas.pokemon import PokemonSchema, SyncRequestSchema, SyncResponseSchema
from app.repositories.pokemon import PokemonRepository
from app.services.pokeapi.client import PokeApiClient
from app.services.pokeapi.formatter import PokeAPIFormatter
from app.services.pokemon.service import record_schema, PokemonService

blp = Blueprint(
    "Pokemon",
    __name__,
    url_prefix="/api/pokemon",
    description="Retrieve, sync, and export Pokémon scouting data.",
)


def get_service() -> PokemonService:
    """Instantiate (or reuse) the pokemon service for the current request."""
    client = PokeApiClient(
        base_url=current_app.config["POKEAPI_BASE_URL"],
        timeout=current_app.config["POKEAPI_TIMEOUT"],
    )
    repository = PokemonRepository()
    formatter = PokeAPIFormatter()
    return PokemonService(client, repository, formatter)


@blp.route("/")
class PokemonCollection(MethodView):
    @blp.response(200, PokemonSchema(many=True))
    def get(self):
        """Return all Pokémon persisted in the database."""
        repo = PokemonRepository()
        return [record_schema(record) for record in repo.list_all()]

    @blp.arguments(SyncRequestSchema)
    @blp.response(200, SyncResponseSchema)
    def post(self, payload):
        """Synchronize Pokémon records with PokeAPI."""
        service = get_service()
        result = service.sync(payload["names"])
        return {"synced": result.synced, "errors": result.errors}
