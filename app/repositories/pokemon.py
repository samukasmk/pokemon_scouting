"""Data access helpers for Pokémon records."""
from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import RepositoryError
from app.extensions import db
from app.models import Pokemon
from app.utils.naming import normalize_name


class PokemonRepository:
    """Repository abstraction around the Pokemon model."""

    def __init__(self, session=None):
        self.session = session or db.session

    def list_all(self) -> list[Pokemon]:
        """List all Pokémon records in the database."""
        return Pokemon.query.order_by(Pokemon.name).all()

    def get_by_name(self, name: str) -> Pokemon | None:
        """Retrieve a Pokémon by its name."""
        name = normalize_name(name)
        return Pokemon.query.filter(Pokemon.name == name).first()

    def upsert(self, payload: dict) -> Pokemon:
        """Create or Update a Pokémon record."""
        try:
            record = self.get_by_name(payload["name"])

            # create db record if not exists
            if record is None:
                record = Pokemon(**payload)
                self.session.add(record)

            # update db record if exists
            else:
                record.update_from_payload(payload)

            self.session.commit()
            return record
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise RepositoryError("Failed to persist Pokémon data") from exc

    def delete_all(self) -> int:
        """Delete all Pokémon records in the database."""
        try:
            count = Pokemon.query.delete()
            self.session.commit()
            return count
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise RepositoryError("Failed to delete Pokémon data") from exc
