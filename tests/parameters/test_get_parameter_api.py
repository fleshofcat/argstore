import pytest
from requests import Session
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


@pytest.mark.parametrize("bad_type", [" ", "type", "float"])
def test_get_parameter_with_invalid_type(client: TestClient, username, bad_type):
    get_param_response = client.get(f"/api/parameters/{username}/param_name/{bad_type}")
    assert get_param_response.status_code == 422
    assert "detail" in get_param_response.json()


def test_get_parameter_without_type(client: Session, username):
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


@pytest.mark.parametrize("typename", ["int", "str"])
def test_get_not_existing_parameter(client: TestClient, typename, username):
    not_existing_parameter_response = client.get(
        f"/api/parameters/{username}/not_exiting_parameter/{typename}"
    )

    assert not_existing_parameter_response.status_code == 200
    assert not_existing_parameter_response.json() == []


def test_get_parameter_with_invalid_user(client: TestClient):
    param_with_invalid_user_response = client.get(
        "/api/parameters/not_existing_user/param_name/str"
    )
    assert param_with_invalid_user_response.status_code == 404
    assert "User" in param_with_invalid_user_response.json()["detail"]
    assert "not found" in param_with_invalid_user_response.json()["detail"]
