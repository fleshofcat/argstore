from starlette.testclient import TestClient


def test_create_parameter(client: TestClient):
    response = client.post("/parameters", json={"name": "param_name", "value": 20})
    assert response.status_code == 201, response.reason
    assert False, "The test must check that new param is appeared"
