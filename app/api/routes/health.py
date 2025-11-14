"""Health check endpoint."""
from __future__ import annotations

from flask import current_app
from flask_smorest import Blueprint

blp = Blueprint(
    "Health",
    __name__,
    url_prefix="/health",
    description="Service level health checks",
)


@blp.route("/")
def health():
    return {
        "status": "ok",
        "app": current_app.config["API_TITLE"],
        "version": current_app.config["API_VERSION"],
    }
