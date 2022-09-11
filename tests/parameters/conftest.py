import pytest
from starlette.testclient import TestClient

from argstore.parameters.schemas import Parameter


class ClientSideParameter(Parameter):
    class Config:
        orm_mode = False


@pytest.fixture
def existed_param(client) -> ClientSideParameter:
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
