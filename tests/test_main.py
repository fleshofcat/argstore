from starlette.testclient import TestClient


def test_redirect_to_docs_from_root(client: TestClient):
    response = client.get("/")
    assert response.ok
    assert response.url.endswith("/docs")
