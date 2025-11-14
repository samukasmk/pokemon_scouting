def record_schema(record) -> dict:
    """Serialize a Pokemon model to dict without relying on Marshmallow."""
    return {
        "id": record.id,
        "pokedex_id": record.pokedex_id,
        "name": record.name,
        "base_experience": record.base_experience,
        "height": record.height,
        "weight": record.weight,
        "abilities": record.abilities,
        "types": record.types,
        "stats": record.stats,
        "sprite": record.sprite,
        "captured_at": record.captured_at,
    }
