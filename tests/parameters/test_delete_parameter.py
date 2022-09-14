from starlette.testclient import TestClient


def test_delete_parameter(client: TestClient, username: str):
    param_url = f"/api/parameters/{username}/param_to_delete/str"
    client.post(param_url, data="val", headers={"Content-type": "text/plain"})

    assert client.delete(param_url).status_code == 204
    assert client.delete(param_url).status_code == 404
