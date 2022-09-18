from starlette.testclient import TestClient


def test_get_all_user_parameters(client: TestClient, username: str):
    h = {"Content-type": "text/plain"}
    client.post(f"/api/parameters/{username}/param1/str", data="val1", headers=h)
    client.post(f"/api/parameters/{username}/param2/int", data="2", headers=h)
    client.post(f"/api/parameters/{username}/param3/str", data="val3", headers=h)
    client.post(f"/api/parameters/{username}/param4/int", data="4", headers=h)

    all_user_params = client.get(f"/api/parameters/{username}/")

    assert all_user_params.status_code == 200, all_user_params.reason
    assert all_user_params.json() == [
        {
            "Name": "param1",
            "Type": "str",
            "Value": "val1",
        },
        {
            "Name": "param2",
            "Type": "int",
            "Value": "2",
        },
        {
            "Name": "param3",
            "Type": "str",
            "Value": "val3",
        },
        {
            "Name": "param4",
            "Type": "int",
            "Value": "4",
        },
    ]


def test_get_all_parameters_of_user_without_parameters(client: TestClient):
    client.post("/users_api/users/", json={"Name": "user_without_params"})

    params_of_new_user_response = client.get("/api/parameters/user_without_params")
    assert params_of_new_user_response.status_code == 200
    assert params_of_new_user_response.json() == []


def test_get_all_parameters_of_not_existing_user(client: TestClient):
    params_not_existing_user_response = client.get("/api/parameters/not_existing_user")
    assert params_not_existing_user_response.status_code == 404
    assert "detail" in params_not_existing_user_response.json()
