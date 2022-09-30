from requests import Session


def test_delete_parameter(client: Session, username: str):
    param_url = f"/api/parameters/{username}/param_to_delete/str"
    client.post(param_url, data="val", headers={"Content-type": "text/plain"})

    assert client.delete(param_url).status_code == 204
    assert client.delete(param_url).status_code == 404


def test_delete_parameter_with_bad_user(client: Session):
    assert (
        client.delete(
            "/api/parameters/not_existing_user/param_to_delete/str"
        ).status_code
        == 404
    )


def test_delete_parameter_with_bad_typename(client: Session, username: str):
    assert (
        client.delete(
            f"/api/parameters/{username}/param_to_delete/bad_type"
        ).status_code
        == 422
    )
