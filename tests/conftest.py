"""Configuration file for Pytest"""
import pytest

from api.app import init_app


@pytest.fixture
def api(loop, aiohttp_client):
    app = loop.run_until_complete(init_app())
    yield loop.run_until_complete(aiohttp_client(app))
    loop.run_until_complete(app.shutdown())
