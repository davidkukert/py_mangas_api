import pytest
from fastapi.testclient import TestClient

from py_mangas_api.app import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
