"""Home endpoints."""
from __future__ import annotations

from flask import redirect
from flask_smorest import Blueprint

blp = Blueprint(
    "Home",
    __name__,
    url_prefix="",
    description="Landing endpoints.",
)


@blp.route("/")
def redirect_to_docs():
    """Redirect root traffic to the interactive API documentation."""
    return redirect("/api/docs")

