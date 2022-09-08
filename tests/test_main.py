import pytest
from starlette.testclient import TestClient

from argstore.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


def test_redirect_to_docs_from_root(client: TestClient):
    response = client.get("/")
    assert response.ok
    assert response.url.endswith("/docs")
