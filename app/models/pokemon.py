"""Database models."""
from __future__ import annotations

from datetime import datetime, UTC

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON

from app.extensions.database import db


class Pokemon(db.Model):
    """Persisted representation of a Pokémon record."""

    __tablename__ = "pokemon"

    id = db.Column(Integer, primary_key=True)
    pokedex_id = db.Column(Integer, nullable=False, unique=True)
    name = db.Column(String(64), nullable=False, unique=True, index=True)
    base_experience = db.Column(Integer, nullable=False)
    height = db.Column(Integer, nullable=False)
    weight = db.Column(Integer, nullable=False)
    abilities = db.Column(JSON, nullable=False)
    types = db.Column(JSON, nullable=False)
    stats = db.Column(JSON, nullable=False)
    sprite = db.Column(Text, nullable=True)
    captured_at = db.Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    def update_from_payload(self, payload: dict) -> None:
        """Update model fields from a sanitized payload."""
        for field, value in payload.items():
            setattr(self, field, value)
