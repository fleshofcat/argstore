from pydantic import parse_obj_as
from starlette.testclient import TestClient

from argstore.parameters.schemas import Parameter


def test_create_parameter(client: TestClient):
    response = client.post("/parameters", json={"name": "param_name", "value": 20})
    assert response.status_code == 201, response.reason
    assert False, "The test must check that new param is appeared"


class ClientSideParameter(Parameter):
    class Config:
        orm_mode = False


def test_read_parameters(client: TestClient):
    response = client.get("/parameters")
    assert response.status_code == 200
    assert parse_obj_as(list[ClientSideParameter], response.json())
