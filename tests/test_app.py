import os

from pytest_mock import MockFixture
from requests import Session
from starlette.testclient import TestClient

from argstore.app import app
from argstore.database import Base


def test_redirect_to_docs_from_root(client_without_db: Session):
    response = client_without_db.get("/")
    assert response.status_code == 200
    assert response.url.endswith("/docs")


def test_init_db_if_necessary(mocker: MockFixture, db_is_not_initialized):
    metadata_mock = mocker.patch.object(Base, "metadata")
    db_name = "db_to_test_auto_init.db"

    mocker.patch.dict(
        os.environ,
        {
            "SQLALCHEMY_DATABASE_URL": f"sqlite:///{db_name}",
            "INIT_NOT_EXISTED_DB": "True",
        },
    )

    with TestClient(app):
        assert metadata_mock.create_all.called


def test_init_db_with_existed_db(mocker: MockFixture, use_test_db):
    from argstore.database import _engine

    db_url = str(_engine.url)  # type: ignore

    metadata_mock = mocker.patch.object(Base, "metadata")
    mocker.patch.dict(
        os.environ,
        {"SQLALCHEMY_DATABASE_URL": db_url, "INIT_NOT_EXISTED_DB": "True"},
    )

    with TestClient(app):
        assert not metadata_mock.create_all.called


def test_init_db_when_it_is_disabled(mocker: MockFixture):
    metadata_mock = mocker.patch.object(Base, "metadata")

    mocker.patch.dict(
        os.environ,
        {
            "SQLALCHEMY_DATABASE_URL": "sqlite:///db_to_test_disabled_auto_init.db",
            "INIT_NOT_EXISTED_DB": "False",
        },
    )

    with TestClient(app):
        assert not metadata_mock.create_all.called


def test_init_db_with_no_db_specified(mocker: MockFixture):
    metadata_mock = mocker.patch.object(Base, "metadata")
    mocker.patch.dict(
        os.environ, {"SQLALCHEMY_DATABASE_URL": "", "INIT_NOT_EXISTED_DB": "True"}
    )

    with TestClient(app):
        assert not metadata_mock.create_all.called
