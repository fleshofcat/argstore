from pydantic import parse_obj_as
from starlette.testclient import TestClient

from argstore.parameters.schemas import Parameter


class ClientSideParameter(Parameter):
    class Config:
        orm_mode = False


def test_create_parameter(client: TestClient):
    to_create = {"name": "param_name", "value": 20}
    response = client.post("/parameters", json=to_create)
    assert response.status_code == 201, response.reason

    created_object = ClientSideParameter(**response.json())
    assert created_object.name == to_create["name"]

    assert False, "The db check also must be there"


def test_read_parameters(client: TestClient):
    response = client.get("/parameters")
    assert response.status_code == 200, response.reason
    assert parse_obj_as(list[ClientSideParameter], response.json())


def test_read_parameter(client: TestClient):
    assert (existed_id := client.get("/parameters").json()[0]["id"])
    response = client.get(f"/parameters/{existed_id}")
    assert response.status_code == 200, response.reason
    assert ClientSideParameter(**response.json())


def test_read_not_existing_parameter(client: TestClient):
    client.delete(f"/parameters/{0}")
    response = client.get(f"/parameters/{0}")
    assert response.status_code == 404
    assert "detail" in response.json()
