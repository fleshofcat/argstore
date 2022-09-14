from starlette.testclient import TestClient


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


invalid_params = [
    {},
    [],
    [1, "2"],
    None,
    {"invalid": "structure"},
]


def test_set_parameters_with_json_api_with_invalid_payload(client: TestClient):
    assert False


def test_set_parameters_with_json_api_with_invalid_user(client: TestClient):
    assert False
