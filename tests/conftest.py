import os
import pytest
from dotenv import dotenv_values


@pytest.fixture
def dot_env() -> dict:
    """.env by default"""
    return dotenv_values()


@pytest.fixture
def env_context(dot_env, monkeypatch):
    """Get env file .env"""
    for k, v in dot_env.items():
        monkeypatch.setenv(k, v)
        # DEBUG
        # print(f'setting {k} to {v}')
