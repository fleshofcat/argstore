import pytest
from starlette.testclient import TestClient


@pytest.fixture(scope="session")
def username(client: TestClient):
    user = "test_parameters_api_username"
    try:
        return client.get(f"/api/users/{user}").json()["Name"]
    except KeyError:
        return client.post("/api/users/", json={"Name": user}).json()["Name"]


@pytest.fixture(params=[("str", "old_val"), ("int", "0")])
def param_existing_for_user(client: TestClient, username: str, request):
    typename, old_value = request.param
    client.post(
        f"/api/parameters/{username}/param_name/{typename}",
        data=old_value,
        headers={"Content-type": "text/plain"},
    )
    return "param_name", username, typename, old_value
