import os

import pytest
from starlette.testclient import TestClient

from argstore.database import Base, create_db_engine
from argstore.main import app


# noinspection PyUnusedLocal
def pytest_make_parametrize_id(config, val):

    if callable(val) and hasattr(val, "__name__"):
        return repr(val.__name__)

    return repr(val)


@pytest.fixture(scope="session")
def use_test_db():
    db_filename = "./test.db"
    engine = create_db_engine(sqlalchemy_database_url=f"sqlite:///{db_filename}")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    os.remove(db_filename)  # Comment it to save the db with test results


@pytest.fixture(scope="session")
def client(use_test_db) -> TestClient:
    return TestClient(app)
