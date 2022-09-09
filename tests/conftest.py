import pytest
from starlette.testclient import TestClient

from argstore.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
