"""Marshmallow schemas for Pokémon endpoints."""
from __future__ import annotations

from marshmallow import Schema, fields, validates_schema, ValidationError


class PokemonSchema(Schema):
    id = fields.Int(dump_only=True)
    pokedex_id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    base_experience = fields.Int(required=True)
    height = fields.Int(required=True)
    weight = fields.Int(required=True)
    abilities = fields.List(fields.Str(), required=True)
    types = fields.List(fields.Str(), required=True)
    stats = fields.Dict(keys=fields.Str(), values=fields.Int(), required=True)
    sprite = fields.Url(allow_none=True)
    captured_at = fields.DateTime(dump_only=True)


class SyncRequestSchema(Schema):
    names = fields.List(fields.Str(), required=True, metadata={"description": "List of Pokémon names"})

    @validates_schema
    def validate_names(self, data, **kwargs):
        names = data.get("names", [])
        if not names:
            raise ValidationError("At least one Pokémon name is required", "names")


class SyncResponseSchema(Schema):
    synced = fields.List(fields.Nested(PokemonSchema), required=True)
    errors = fields.Dict(
        keys=fields.Str(),
        values=fields.Str(),
        required=True,
        metadata={"description": "Failed Pokémon keyed by their provided names"},
    )

