from starlette.testclient import TestClient


def test_redirect_to_docs_from_root(client_without_db: TestClient):
    response = client_without_db.get("/")
    assert response.ok
    assert response.url.endswith("/docs")
