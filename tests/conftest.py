import os

import pytest
from pydantic import BaseSettings
from requests_toolbelt import sessions
from starlette.testclient import TestClient

from argstore import database
from argstore.app import app
from argstore.database import Base, create_db_engine


# noinspection PyUnusedLocal
def pytest_make_parametrize_id(config, val):

    if callable(val) and hasattr(val, "__name__"):
        return repr(val.__name__)

    return repr(val)


class SettingsForTest(BaseSettings):
    url_to_test: str = ""

    class Config:
        env_file = ".env", "../.env"


@pytest.fixture(scope="session")
def settings_for_test() -> SettingsForTest:
    return SettingsForTest()


@pytest.fixture(scope="session")
def use_test_db():
    db_filename = "./test.db"
    engine = create_db_engine(sqlalchemy_database_url=f"sqlite:///{db_filename}")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    os.remove(db_filename)  # Comment it to save the db with test results


@pytest.fixture(scope="session")
def client_without_db() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")  # TODO Change TestClient to Session in type hints
def client(client_without_db, use_test_db, settings_for_test) -> TestClient:
    if settings_for_test.url_to_test:
        with sessions.BaseUrlSession(base_url=settings_for_test.url_to_test) as s:
            yield s
    else:
        now_it_is_a_client_with_db = client_without_db
        yield now_it_is_a_client_with_db


@pytest.fixture
def db_is_not_initialized():
    # noinspection PyProtectedMember
    old_engine = database._engine

    # noinspection PyProtectedMember
    old_SessionFabric = database._SessionFabric

    database._engine = None
    database._SessionFabric = None

    yield

    database._engine = old_engine
    database._SessionFabric = old_SessionFabric
