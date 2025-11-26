"""Flask extension instances."""

from __future__ import annotations

import os

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


# class BaseSchema(SQLAlchemyAutoSchema):
#     """Base SQLAlchemy schema providing shared Meta options."""
#
#     class Meta:
#         load_instance = True
#         sqla_session = db.session


def init_app(app):
    # fix db uri path according to full path of current directory in different scenarios
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite:") and not db_uri.endswith(":memory:"):
        db_file = app.config["SQLALCHEMY_DATABASE_URI"].split("/")[-1]
        db_path = os.path.join(app.instance_path, db_file)
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # initialize db connection
    db.init_app(app)

    # create db tables if not exists
    with app.app_context():
        db.create_all()
