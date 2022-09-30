import pytest
from requests import Session


@pytest.fixture(scope="session")
def username(client: Session):
    user = "test_parameters_api_username"
    try:
        return client.get(f"/users_api/users/{user}").json()["Name"]
    except KeyError:
        return client.post("/users_api/users/", json={"Name": user}).json()["Name"]


@pytest.fixture(params=[("str", "old_val"), ("int", "0")])
def param_existing_for_user(client: Session, username: str, request):
    typename, old_value = request.param
    client.post(
        f"/api/parameters/{username}/param_name/{typename}",
        data=old_value,
        headers={"Content-type": "text/plain"},
    )
    return "param_name", username, typename, old_value
