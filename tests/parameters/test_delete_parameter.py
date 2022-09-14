from starlette.testclient import TestClient


def test_delete_parameter(client: TestClient, existed_param):
    assert client.delete(f"/parameters/{existed_param.id}").status_code == 204
    assert client.delete(f"/parameters/{existed_param.id}").status_code == 404

    assert "detail" in client.delete(f"/parameters/{existed_param.id}").json()
