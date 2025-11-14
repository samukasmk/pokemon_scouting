"""API blueprint exposing Pokémon resources."""
from __future__ import annotations
from flask.views import MethodView
from flask_smorest import Blueprint
from app.api.schemas.pokemon import PokemonSchema
from app.repositories.pokemon import PokemonRepository
from app.services.pokemon.service import record_schema

blp = Blueprint(
    "Pokemon",
    __name__,
    url_prefix="/api/pokemon",
    description="Retrieve, sync, and export Pokémon scouting data.",
)


@blp.route("/")
class PokemonCollection(MethodView):
    @blp.response(200, PokemonSchema(many=True))
    def get(self):
        """Return all Pokémon persisted in the database."""
        repo = PokemonRepository()
        return [record_schema(record) for record in repo.list_all()]
