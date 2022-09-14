import pytest
from pydantic import BaseModel, parse_obj_as, validator
from starlette.testclient import TestClient

from tests.parameters.conftest import ClientSideParameter


def test_get_parameter(client: TestClient):
    typename = "str"
    client.get(f"/api/parameters/<user>/<имя параметра>/{typename}")

    class Param(BaseModel):
        Name: str
        Type: str

        @validator("Type")
        def type_mast_be_str_or_int(cls, type_name):
            if type_name not in ("str", "int"):
                raise ValueError(
                    f"Type mast be 'str' or 'int', got '{type_name}' instead"
                )
            return type_name

    assert "list[Parameter](**response.json())"
    assert "param.Name == 'used_name'"
    assert "param.Type == 'used_type'"
    assert "param.Value == 'expected_value'"


def test_get_parameter_without_type(client: TestClient):
    client.get("/api/parameters/<user>/<имя параметра>/")
    assert "cast response.json() to list[Parameter]"
    assert "result not empty"


@pytest.mark.parametrize("valid_type", ["", "str"])
def test_get_not_existing_parameter(client: TestClient, valid_type):
    not_exiting_parameter = ""
    client.get(f"/api/parameters/<user>/{not_exiting_parameter}/{valid_type}")
    assert "response.json() == []"


@pytest.mark.parametrize("invalid_user", ["", "not_existing_user"])
@pytest.mark.parametrize("valid_type", ["", "str"])
def test_get_parameter_with_invalid_user(client: TestClient, invalid_user, valid_type):
    client.get(f"/api/parameters/{invalid_user}/<имя параметра>/{valid_type}")
    assert "404 User not found"


# ----------------------------------------------------------


def test_get_all_user_parameters(client: TestClient):
    client.get("/api/parameters/<user_with_params>")
    assert "cast r.json() to list[Parameter]"
    assert "params != []"


def test_get_all_parameters_of_user_without_parameters(client: TestClient):
    client.get("/api/parameters/<user_without_params>")
    assert "r.json() == []"


# -----------------------------------------------------


def test_set_parameters_with_json_api(client: TestClient):
    created_params = client.post(
        "/api/<existing_user>",
        json={
            "Query": [
                {
                    "Operation": "SetParam",
                    "Name": "<имя параметра>",
                    "Type": "<тип параметра>",
                    "Value": "<значение параметра>",
                },
                {
                    "Operation": "SetParam",
                    "Name": "<имя параметра>",
                    "Type": "<тип параметра>",
                    "Value": "<значение параметра>",
                },
            ]
        },
    ).json()
    assert created_params.status_code == 201
    assert "created_params are as expected"
    assert "Re-requested params == created_params"


def test_set_parameters_with_json_api_with_invalid_payload(client: TestClient):
    assert False


def test_set_parameters_with_json_api_with_invalid_user(client: TestClient):
    assert False


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
