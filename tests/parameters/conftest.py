import pytest
from pydantic import ValidationError
from starlette.testclient import TestClient

from argstore.parameters.schemas import Parameter


class ClientSideParameter(Parameter):
    class Config:
        orm_mode = False


@pytest.fixture(scope="session")
def username(client: TestClient):
    user = "test_set_parameters_api_username"
    try:
        return client.get(f"/api/users/{user}").json()["Name"]
    except ValidationError:
        return client.post("/api/users/", json={"Name": user}).json()["Name"]


@pytest.fixture
def existed_param(client, username) -> ClientSideParameter:
    response = client.post(
        "/parameters",
        json={
            "name": "some_name",
            "value": "some_value",
        },
        allow_redirects=True,
    )
    assert response.status_code == 201, response.reason
    return ClientSideParameter(**response.json())


@pytest.fixture
def not_existed_param_id(client: TestClient) -> int:
    client.delete(f"/parameters/{0}")
    return 0


@pytest.fixture
def make_sure_there_are_some_params(existed_param):
    pass


@pytest.fixture(params=[("str", "old_val"), ("int", "0")])
def param_existing_for_user(client: TestClient, username: str, request):
    typename, old_value = request.param
    client.post(
        f"/api/parameters/{username}/param_name/{typename}",
        data=old_value,
        headers={"Content-type": "text/plain"},
    )
    return "param_name", username, typename, old_value
