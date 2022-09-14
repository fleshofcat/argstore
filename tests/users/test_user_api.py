from starlette.testclient import TestClient


def test_create_read_user(client: TestClient):
    bob_response = client.post("/api/users/", json={"Name": "Bob"})
    assert bob_response.status_code == 201, bob_response.reason
    assert bob_response.json() == {"Name": "Bob", "Parameters": []}
    assert client.get("/api/users/Bob").json() == bob_response.json()


def test_read_users(client: TestClient):
    client.post("/api/users/", json={"Name": "Alice"})
    client.post("/api/users/", json={"Name": "John"})

    client.post(
        "/api/parameters/John/param_of_john/str",
        data="val",
        headers={"Content-type": "text/plain"},
    )

    users_response = client.get("/api/users/")
    assert users_response.status_code == 200

    users = users_response.json()

    assert type(users) is list
    assert {"Name": "Alice", "Parameters": []} in users
    assert {
        "Name": "John",
        "Parameters": [{"Name": "param_of_john", "Type": "str", "Value": "val"}],
    } in users

    # Test skip arg
    assert len(client.get("/api/users/", params={"skip": len(users) - 1}).json()) == 1

    # Test limit arg
    assert len(client.get("/api/users/", params={"limit": 1}).json()) == 1
