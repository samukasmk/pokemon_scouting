"""Application factory."""
from __future__ import annotations

import os

from dynaconf import FlaskDynaconf
from flask import Flask

from app import cli
from app.api.routes.health import blp as health_blp
from app.api.routes.home import blp as home_blp
from app.api.routes.pokemon import blp as pokemon_blp
from app.extensions import api, db, register_error_handlers


def create_app(config_env: str | None = None) -> Flask:
    app = Flask(__name__)

    # configure Dynaconf (ENV_FOR_DYNACONF drives environment selection)
    env_name = config_env or os.environ.get("ENV_FOR_DYNACONF") or "default"
    os.environ["ENV_FOR_DYNACONF"] = env_name

    # initialize dynaconf integration
    FlaskDynaconf(
        app,
        settings_files=["settings.toml", ".secrets.toml"],
        env_switcher="ENV_FOR_DYNACONF",
        environments=True,
        load_dotenv=True,
        envvar_prefix="POKEMON",
    )

    # fix db uri path according to full path of current directory in different scenarios
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite:") and not db_uri.endswith(":memory:"):
        db_file = app.config["SQLALCHEMY_DATABASE_URI"].split("/")[-1]
        db_path = os.path.join(app.instance_path, db_file)
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # register error pages when received exceptions
    register_error_handlers(app)

    # ensure JSON responses keep schema field order
    app.json.sort_keys = False

    # initialize db connection
    db.init_app(app)

    # initialize flask_smorest api
    api.init_app(app)

    # create db tables if not exists
    with app.app_context():
        db.create_all()

    # initialize api blueprints
    api.register_blueprint(home_blp)
    api.register_blueprint(health_blp)
    api.register_blueprint(pokemon_blp)

    # initialize cli commands
    cli.init_app(app)

    return app
