from starlette.testclient import TestClient


def test_create_read_user(client: TestClient):
    bob_response = client.post("/users_api/users/", json={"Name": "Bob"})
    assert bob_response.status_code == 201, bob_response.reason
    assert bob_response.json() == {"Name": "Bob", "Parameters": []}
    assert client.get("/users_api/users/Bob").json() == bob_response.json()


def test_recreate_existing_user(client: TestClient):
    new_user = client.post("/users_api/users/", json={"Name": "user_to_re_create"})
    assert new_user.status_code in (201, 409), new_user.json()
    recreated = client.post("/users_api/users/", json={"Name": "user_to_re_create"})
    assert recreated.status_code == 409, recreated.json()


def test_read_not_existing_user(client: TestClient):
    assert client.get("/users_api/users/not_existing_user").status_code == 404


def test_read_users(client: TestClient):
    client.post("/users_api/users/", json={"Name": "Alice"})
    client.post("/users_api/users/", json={"Name": "John"})

    client.post(
        "/api/parameters/John/param_of_john/str",
        data="val",
        headers={"Content-type": "text/plain"},
    )

    users_response = client.get("/users_api/users/")
    assert users_response.status_code == 200

    users = users_response.json()

    assert type(users) is list
    assert {"Name": "Alice", "Parameters": []} in users
    assert {
        "Name": "John",
        "Parameters": [{"Name": "param_of_john", "Type": "str", "Value": "val"}],
    } in users

    # Test skip arg
    assert (
        len(client.get("/users_api/users/", params={"skip": len(users) - 1}).json())
        == 1
    )

    # Test limit arg
    assert len(client.get("/users_api/users/", params={"limit": 1}).json()) == 1


def test_delete_user(client: TestClient):
    client.post("/users_api/users/", json={"Name": "user_to_del"})
    assert client.get("/users_api/users/user_to_del").status_code == 200

    assert client.delete("/users_api/users/user_to_del").status_code == 204
    assert client.delete("/users_api/users/user_to_del").status_code == 404

    assert client.get("/users_api/users/user_to_del").status_code == 404
