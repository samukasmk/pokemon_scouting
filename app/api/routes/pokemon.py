"""API blueprint exposing Pokémon resources."""
from __future__ import annotations

from flask import current_app, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.api.schemas.pokemon import PokemonSchema, SyncRequestSchema, SyncResponseSchema
from app.core.exceptions import PokemonSyncError
from app.repositories.pokemon import PokemonRepository
from app.services.pokeapi.client import PokeApiClient
from app.services.pokeapi.formatter import PokeAPIFormatter
from app.services.pokemon.service import PokemonService

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
        return repo.list_all()

    @blp.arguments(SyncRequestSchema)
    @blp.response(200, SyncResponseSchema)
    def post(self, payload):
        """Synchronize Pokémon records with PokeAPI."""
        service = get_service()
        result = service.sync(payload["names"])
        return result


@blp.route("/<string:name>")
class PokemonResource(MethodView):
    @blp.response(200, PokemonSchema)
    def get(self, name: str):
        """Return a single Pokémon, refreshing from PokeAPI if requested."""
        repo = PokemonRepository()

        # get refresh argument from query params
        refresh = request.args.get("refresh", "false").lower() == "true"

        # try to find Pokémon in local db
        record = repo.get_by_name(name)
        if record and not refresh:
            return record

        # if not found get from PokeAPI and save in db
        service = get_service()
        try:
            result = service.sync([name])
        except PokemonSyncError as exc:
            abort(404, message=str(exc), errors=exc.errors)

        return result.synced[0]
