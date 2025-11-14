from __future__ import annotations

from app.config import BaseConfig, TestingConfig, get_config


def test_get_config_defaults():
    assert get_config() is BaseConfig
    assert get_config("testing") is TestingConfig
    assert get_config("missing") is BaseConfig
