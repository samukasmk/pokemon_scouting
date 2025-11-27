"""Application factory."""
from __future__ import annotations

from flask import Flask

from app.extensions import flask_dynaconf, database, error_handlers, json_sort_keys, blueprints, commands, celery


def create_app(config_env: str | None = None) -> Flask:
    app = Flask(__name__)

    # initialize flask extensions
    flask_dynaconf.init_app(app, config_env)
    database.init_app(app)
    error_handlers.init_app(app)
    json_sort_keys.init_app(app)
    blueprints.init_app(app)
    commands.init_app(app)
    celery.init_app(app)

    return app
