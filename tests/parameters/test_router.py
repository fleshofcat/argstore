from starlette.testclient import TestClient


def test_create_parameter(client: TestClient):
    response = client.post("/parameter", json={"name": "param_name", "value": 20})
    assert response.ok
    assert False, "The test must check that new param is appeared"
