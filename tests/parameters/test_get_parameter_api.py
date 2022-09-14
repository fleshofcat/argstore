import pytest
from starlette.testclient import TestClient


def test_get_parameter(client: TestClient, param_existing_for_user):
    param_name, user, typename, value = param_existing_for_user

    get_param_response = client.get(f"/api/parameters/{user}/{param_name}/{typename}")
    assert get_param_response.status_code == 200

    assert get_param_response.json() == [
        {
            "Name": param_name,
            "Type": typename,
            "Value": value,
        }
    ]


def test_get_parameter_without_type(client: TestClient, username):
    param = "param_to_test_get_without_type"
    h = {"Content-type": "text/plain"}
    client.post(f"/api/parameters/{username}/{param}/str", data="val", headers=h)
    client.post(f"/api/parameters/{username}/{param}/int", data="1", headers=h)

    param_without_type_response = client.get(f"/api/parameters/{username}/{param}")

    assert param_without_type_response.status_code == 200
    assert param_without_type_response.json() == [
        {
            "Name": param,
            "Type": "str",
            "Value": "val",
        },
        {
            "Name": param,
            "Type": "int",
            "Value": "1",
        },
    ]


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
