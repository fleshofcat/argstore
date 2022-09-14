from starlette.testclient import TestClient


def test_create_read_user(client: TestClient):
    bob_response = client.post("/api/users/", json={"Name": "Bob"})
    assert bob_response.status_code == 201, bob_response.reason
    assert bob_response.json() == {"Name": "Bob", "Parameters": []}
    assert client.get("/api/users/Bob").json() == bob_response.json()
