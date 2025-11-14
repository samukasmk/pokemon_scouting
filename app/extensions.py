"""Flask extension instances."""

from __future__ import annotations

from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.core.exceptions import AppError

db = SQLAlchemy()
api = Api()


class BaseSchema(SQLAlchemyAutoSchema):
    """Base SQLAlchemy schema providing shared Meta options."""

    class Meta:
        load_instance = True
        sqla_session = db.session


def register_error_handlers(app):
    """Attach global error handlers to the application."""

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        return {"errors": exc.messages}, 400

    @app.errorhandler(AppError)
    def handle_app_error(exc: AppError):
        payload = {"message": str(exc)}
        errors = getattr(exc, "errors", None)
        if errors:
            payload["errors"] = errors
        return payload, 400

