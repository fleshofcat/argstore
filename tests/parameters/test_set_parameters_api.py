import pytest
from requests import Session


@pytest.fixture(params=[("str", "test_val"), ("int", "1")])
def param_not_existing_for_user(client: Session, username: str, request):
    param_name = "not_existing_name"
    typename, test_value = request.param

    client.delete(f"/api/parameters/{username}/{param_name}/{typename}")
    return param_name, username, typename, test_value


def test_set_new_parameter(client: Session, param_not_existing_for_user):
    not_existing_param_name, user, typename, test_value = param_not_existing_for_user
    url = f"/api/parameters/{user}/{not_existing_param_name}/{typename}"

    create_param_response = client.post(
        url, data=test_value, headers={"Content-type": "text/plain"}
    )

    assert create_param_response.status_code == 201
    assert create_param_response.json() == [
        {
            "Name": not_existing_param_name,
            "Type": typename,
            "Value": test_value,
        }
    ]

    assert client.get(url).json() == create_param_response.json()


def test_update_parameter(client: Session, param_existing_for_user):
    param, user, typename, old_value = param_existing_for_user
    new_value = old_value * 2

    updated_param_response = client.post(
        f"/api/parameters/{user}/{param}/{typename}",
        data=new_value,
        headers={"Content-type": "text/plain"},
    )
    assert updated_param_response.status_code == 200
    assert updated_param_response.json()[0]["Value"] == new_value
    assert (
        client.get(f"/api/parameters/{user}/{param}/{typename}").json()
        == updated_param_response.json()
    )


@pytest.mark.parametrize("not_valid_type", ["float", "qwerty", "1"])
def test_set_parameter_with_not_valid_type(
    client: Session, username: str, not_valid_type
):
    param = "parameter_with_not_valid_type"
    set_with_not_valid_type_response = client.post(
        f"/api/parameters/{username}/{param}/{not_valid_type}",
        data="value",
        headers={"Content-type": "text/plain"},
    )
    assert (
        set_with_not_valid_type_response.status_code == 422
    ), set_with_not_valid_type_response.json()
    assert "detail" in set_with_not_valid_type_response.json()


@pytest.fixture(scope="session")
def init_existed_and_not_existed_int_params(client: Session, username: str):
    existed, not_existed = "existed_param", "not_existed_param"
    client.post(
        f"/api/parameters/{username}/{existed}/int",
        data="1",
        headers={"Content-type": "text/plain"},
    )
    client.delete(f"/api/parameters/{username}/{not_existed}/int")
    return existed, not_existed


@pytest.mark.parametrize("param", ["existed_param", "not_existed_param"])
@pytest.mark.parametrize("bad_value", ["value", "1.1", "none", "{}", "[]", ""])
def test_create_parameter_with_type_value_mismatch_for_int(
    client: Session,
    username,
    bad_value,
    param,
    init_existed_and_not_existed_int_params,
):
    """Now only 'int' can be mismatched"""

    create_with_mismatch_response = client.post(
        f"/api/parameters/{username}/{param}/int",
        data=bad_value,
        headers={"Content-type": "text/plain"},
    )
    assert create_with_mismatch_response.status_code == 422
    assert "detail" in create_with_mismatch_response.json()


@pytest.fixture(scope="session")
def not_existing_user(client: Session) -> str:
    not_existing_user = "not_existing_user"
    assert client.delete(f"/api/users/{not_existing_user}").status_code in (204, 404)
    return not_existing_user


@pytest.mark.parametrize("typename", ["str", "int"])
def test_set_parameter_with_not_existing_user(
    client: Session, typename, not_existing_user
):
    url_with_not_existing_user = (
        f"/api/parameters/{not_existing_user}/param_of_not_existing_user/{typename}"
    )
    response = client.post(
        url_with_not_existing_user,
        data="1",
        headers={"Content-type": "text/plain"},
    )

    assert response.status_code == 404
