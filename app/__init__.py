"""Application factory."""
from __future__ import annotations

from flask import Flask

from app import cli
from app.config import get_config
from app.api.routes.health import blp as health_blp
from app.extensions import api, db, register_error_handlers


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    # register error pages when received exceptions
    register_error_handlers(app)

    # define config
    config_class = get_config(config_name or None)
    app.config.from_object(config_class)

    # initialize db connection
    db.init_app(app)

    # initialize flask_smorest api
    api.init_app(app)

    # create db tables if not exists
    with app.app_context():
        db.create_all()

    # initialize api blueprints
    api.register_blueprint(health_blp)

    # initialize cli commands
    cli.init_app(app)

    return app
