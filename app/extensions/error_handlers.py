"""Flask extension instances."""

from __future__ import annotations

from marshmallow import ValidationError

from app.core.exceptions import AppError


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


def init_app(app):
    # register error pages when received exceptions
    register_error_handlers(app)
