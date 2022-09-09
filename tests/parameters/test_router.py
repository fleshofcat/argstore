from pydantic import parse_obj_as
from starlette.testclient import TestClient

from argstore.parameters.schemas import Parameter


class ClientSideParameter(Parameter):
    class Config:
        orm_mode = False


def test_create_parameter(client: TestClient):
    to_create = {"name": "param_name", "value": 20}
    response = client.post("/parameters", json=to_create, allow_redirects=True)
    assert response.status_code == 201, response.reason

    created_object = ClientSideParameter(**response.json())
    assert created_object.name == to_create["name"]
    assert created_object.value == to_create["value"]

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


def test_update_parameter(client: TestClient):
    not_existing_param = {"id": 0, "name": "no_param", "value": 0}
    assert (
        client.put(
            "/parameters", json=not_existing_param, allow_redirects=True
        ).status_code
        == 404
    )

    created_param = client.post(
        "/parameters",
        json={"name": "param_to_update", "value": 11},
        allow_redirects=True,
    ).json()

    assert created_param["id"]

    update_response = client.put(
        "/parameters", json=created_param | {"value": 0}, allow_redirects=True
    )
    assert update_response.status_code == 200

    updated_param = update_response.json()
    assert updated_param["value"] == 0
    assert updated_param["id"] == created_param["id"]
