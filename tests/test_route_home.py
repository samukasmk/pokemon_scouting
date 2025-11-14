"""Tests for the home routes."""
from __future__ import annotations


def test_home_redirects_to_docs(client):
    response = client.get("/")

    assert response.status_code == 302
    assert response.headers["Location"] == "/api/docs"

