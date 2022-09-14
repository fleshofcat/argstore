from starlette.testclient import TestClient


def test_redirect_to_docs_from_root(client_without_db: TestClient):
    response = client_without_db.get("/")
    assert response.status_code == 200
    assert response.url.endswith("/docs")
