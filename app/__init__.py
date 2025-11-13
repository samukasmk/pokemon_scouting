"""Application factory."""
from __future__ import annotations

from flask import Flask

from app import cli
from app.config import get_config
from app.extensions import api, db, register_error_handlers


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    config_class = get_config(config_name or None)
    app.config.from_object(config_class)

    db.init_app(app)
    api.init_app(app)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    cli.init_app(app)
    return app
