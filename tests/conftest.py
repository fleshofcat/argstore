import asyncio
import os

import pytest
from sqlalchemy import create_engine
from starlette.testclient import TestClient

from argstore import database
from argstore.database import Base
from argstore.main import app


# noinspection PyUnusedLocal
def pytest_make_parametrize_id(config, val):

    if callable(val) and hasattr(val, "__name__"):
        return repr(val.__name__)

    return repr(val)


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def use_test_db():

    db_filename = "./test.db"
    database.set_sqlalchemy_database_url(f"sqlite+aiosqlite:///{db_filename}")

    # Tests using the client fixture is about how users work with the API.
    # Which means that no matter what asynchrony is when processing requests,
    # users should be abstracted from this
    # and should be able to work with the service synchronously
    engine = create_engine(
        f"sqlite:///{db_filename}", connect_args={"check_same_thread": False}
    )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    os.remove(db_filename)  # Comment it to save the db with test results


@pytest.fixture(scope="session")
def client_without_db() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def client(client_without_db, use_test_db) -> TestClient:
    now_it_is_a_client_with_db = client_without_db
    return now_it_is_a_client_with_db
