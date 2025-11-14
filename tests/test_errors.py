from __future__ import annotations


def test_validation_error_handler(app):
    resp = app.test_client().get("/__validation")
    assert resp.status_code == 400
    assert "names" in resp.get_json()["errors"]


def test_app_error_handler(app):
    resp = app.test_client().get("/__app_error")
    assert resp.status_code == 400
    body = resp.get_json()
    assert body["message"] == "boom"
    assert "pikachu" in body["errors"]


def test_app_error_handler_without_details(app):
    resp = app.test_client().get("/__app_error_simple")
    assert resp.status_code == 400
    assert resp.get_json() == {"message": "simple-error"}
