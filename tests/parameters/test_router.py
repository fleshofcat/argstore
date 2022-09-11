import pytest
from pydantic import parse_obj_as
from starlette.testclient import TestClient

from tests.parameters.conftest import ClientSideParameter


def test_create_parameter(client: TestClient):
    response = client.post(
        "/parameters", json={"name": "param_name", "value": 20}, allow_redirects=True
    )
    assert response.status_code == 201, response.reason

    created_param = response.json()
    assert created_param["name"] == "param_name"
    assert created_param["value"] == 20

    re_requested_param = client.get(f"/parameters/{created_param['id']}").json()
    assert created_param == re_requested_param


invalid_params = [
    {},
    [],
    [1, "2"],
    None,
    {"invalid": "structure"},
    {"name": "n"},
    {"value": 0},
    {"name": "", "value": 0},
    {"name": 3, "value": 0},
    {"name": "name", "value": 0.1},
    {"name": "name", "value": None},
]


@pytest.mark.parametrize("payload", invalid_params)
def test_create_parameter_with_invalid_payload(client: TestClient, payload: dict):
    response = client.post("/parameters", json=payload, allow_redirects=True)
    assert response.status_code == 422, response.reason
    assert response.reason == "Unprocessable Entity"
    assert "detail" in response.json()


def test_read_parameters(client: TestClient, make_sure_there_are_some_params):
    response = client.get("/parameters")
    assert response.status_code == 200, response.reason
    assert response.json()
    assert parse_obj_as(list[ClientSideParameter], response.json())


def test_read_parameter(client: TestClient, existed_param):
    response = client.get(f"/parameters/{existed_param.id}")
    assert response.status_code == 200, response.reason
    assert ClientSideParameter(**response.json())


def test_read_not_existing_parameter(client: TestClient, not_existed_param_id: int):
    response = client.get(f"/parameters/{not_existed_param_id}")
    assert response.status_code == 404, response.reason
    assert "detail" in response.json()


def test_update_parameter(client: TestClient, existed_param: ClientSideParameter):
    update_payload = existed_param.copy(update={"value": "updated"}).dict()
    update_response = client.put(
        "/parameters", json=update_payload, allow_redirects=True
    )
    assert update_response.status_code == 200, update_response.reason

    updated_param = update_response.json()
    assert updated_param["value"] == "updated"
    assert updated_param == update_payload

    re_requested_updated_param = client.get(f"/parameters/{updated_param['id']}").json()
    assert re_requested_updated_param == updated_param


def test_update_not_existed_parameter(client: TestClient, not_existed_param_id):
    response = client.put(
        "/parameters",
        json={"id": not_existed_param_id, "name": "no_param", "value": 0},
        allow_redirects=True,
    )
    assert response.status_code == 404, response.reason
    assert "detail" in response.json()


@pytest.mark.parametrize("payload", [p for p in invalid_params if type(p) is dict])
def test_update_parameter_with_invalid_payload(
    client: TestClient, existed_param: ClientSideParameter, payload: dict
):
    payload["id"] = existed_param.id
    update_response = client.put("/parameters", json=payload, allow_redirects=True)
    assert update_response.status_code == 422
    assert "detail" in update_response.json()


def test_update_parameter_without_id(
    client: TestClient, existed_param: ClientSideParameter
):
    update_response = client.put(
        "/parameters", json={"name": "name", "value": 1}, allow_redirects=True
    )
    assert update_response.status_code == 422
    assert "detail" in update_response.json()


def test_delete_parameter(client: TestClient, existed_param):
    assert client.delete(f"/parameters/{existed_param.id}").status_code == 204
    assert client.delete(f"/parameters/{existed_param.id}").status_code == 404

    assert "detail" in client.delete(f"/parameters/{existed_param.id}").json()
