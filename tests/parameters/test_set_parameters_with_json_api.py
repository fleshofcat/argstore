import pytest
from starlette.testclient import TestClient


def test_set_parameters_with_json_api(client: TestClient, username: str):
    created_params = client.post(
        f"/api/parameters/{username}",
        json={
            "Query": [
                {
                    "Operation": "SetParam",
                    "Name": "test_json_api_param1",
                    "Type": "str",
                    "Value": "val1",
                },
                {
                    "Operation": "SetParam",
                    "Name": "test_json_api_param2",
                    "Type": "int",
                    "Value": "2",
                },
            ]
        },
    )
    assert created_params.status_code == 200, created_params.json()
    assert created_params.json() == {
        "Result": [
            {
                "Operation": "SetParam",
                "Name": "test_json_api_param1",
                "Type": "str",
                "Status": "OK",
            },
            {
                "Operation": "SetParam",
                "Name": "test_json_api_param2",
                "Type": "int",
                "Status": "OK",
            },
        ]
    }

    assert client.get(
        f"/api/parameters/{username}/test_json_api_param1/str"
    ).json() == [
        {
            "Name": "test_json_api_param1",
            "Type": "str",
            "Value": "val1",
        }
    ]
    assert client.get(
        f"/api/parameters/{username}/test_json_api_param2/int"
    ).json() == [
        {
            "Name": "test_json_api_param2",
            "Type": "int",
            "Value": "2",
        }
    ]


def test_set_parameters_with_json_api_with_operations_on_the_same_parameter(
    client: TestClient, username: str
):
    created_params = client.post(
        f"/api/parameters/{username}",
        json={
            "Query": [
                {
                    "Operation": "SetParam",
                    "Name": "param_to_overwrite",
                    "Type": "str",
                    "Value": "to_overwrite",
                },
                {
                    "Operation": "SetParam",
                    "Name": "param_to_overwrite",
                    "Type": "str",
                    "Value": "overwritten",
                },
            ]
        },
    )

    assert created_params.status_code == 200, created_params.json()
    assert created_params.json() == {
        "Result": [
            {
                "Operation": "SetParam",
                "Name": "param_to_overwrite",
                "Type": "str",
                "Status": "OK",
            },
            {
                "Operation": "SetParam",
                "Name": "param_to_overwrite",
                "Type": "str",
                "Status": "OK",
            },
        ]
    }

    assert client.get(f"/api/parameters/{username}/param_to_overwrite/str").json() == [
        {
            "Name": "param_to_overwrite",
            "Type": "str",
            "Value": "overwritten",
        }
    ]


def test_set_parameters_with_json_api_with_empty_query_list(
    client: TestClient, username: str
):
    created_params = client.post(f"/api/parameters/{username}", json={"Query": []})
    assert created_params.status_code == 200, created_params.json()
    assert created_params.json() == {"Result": []}


@pytest.mark.parametrize(
    "bad_payload",
    [
        {},
        [],
        [1, "2"],
        None,
        {"invalid": "structure"},
        {"Query": {}},
        {"Query": [{}]},
        {"Query": [{"invalid": "structure"}]},
        {
            "Query": [
                {
                    "Operation": "invalid_values",
                    "Name": "param",
                    "Type": "invalid_values",
                    "Value": "val",
                },
            ]
        },
    ],
)
def test_set_parameters_with_json_api_with_invalid_payload(
    client: TestClient, username: str, bad_payload: dict | list
):
    created_params_response = client.post(
        f"/api/parameters/{username}", json=bad_payload
    )
    assert created_params_response.status_code == 422, created_params_response.json()
    assert "detail" in created_params_response.json()


def test_set_parameters_with_json_api_with_invalid_user(client: TestClient):
    created_params = client.post(
        "/api/parameters/not_existed_user",
        json={
            "Query": [
                {
                    "Operation": "SetParam",
                    "Name": "param",
                    "Type": "str",
                    "Value": "val",
                }
            ]
        },
    )
    assert created_params.status_code == 404, created_params.json()
    assert created_params.json() == {
        "Result": [
            {
                "Operation": "SetParam",
                "Name": "param",
                "Type": "str",
                "Status": "ERROR",
            }
        ]
    }
