from pydantic import BaseModel
from requests import Session


def test_get_all_user_parameters(client: Session, username: str):
    h = {"Content-type": "text/plain"}

    class ParamToCreate(BaseModel):
        Name: str
        Type: str
        Value: str

    params_to_create = [
        ParamToCreate(Name="param1", Type="str", Value="val1"),
        ParamToCreate(Name="param2", Type="int", Value="2"),
        ParamToCreate(Name="param3", Type="str", Value="val3"),
        ParamToCreate(Name="param4", Type="int", Value="4"),
    ]

    for param in params_to_create:
        client.post(
            f"/api/parameters/{username}/{param.Name}/{param.Type}",
            data=param.Value,
            headers=h,
        )

    all_user_params = client.get(f"/api/parameters/{username}").json()

    for param in params_to_create:
        assert param.dict() in all_user_params


def test_get_all_parameters_of_user_without_parameters(client: Session):
    client.post("/users_api/users/", json={"Name": "user_without_params"})

    params_of_new_user_response = client.get("/api/parameters/user_without_params")
    assert params_of_new_user_response.status_code == 200
    assert params_of_new_user_response.json() == []


def test_get_all_parameters_of_not_existing_user(client: Session):
    params_not_existing_user_response = client.get("/api/parameters/not_existing_user")
    assert params_not_existing_user_response.status_code == 404
    assert "detail" in params_not_existing_user_response.json()
