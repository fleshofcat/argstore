import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from argstore.database import Base, get_db
from argstore.main import app


# noinspection PyUnusedLocal
def pytest_make_parametrize_id(config, val):

    if callable(val) and hasattr(val, "__name__"):
        return repr(val.__name__)

    return repr(val)


@pytest.fixture(scope="session")
def use_test_db():
    db_filename = "./test.db"
    sqlalchemy_database_url = f"sqlite:///{db_filename}"

    engine = create_engine(
        sqlalchemy_database_url, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def get_test_db():
        db: Session = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    yield
    del app.dependency_overrides[get_db]

    # Comment it to save the db with test results
    os.remove(db_filename)


@pytest.fixture(scope="session")
def client(use_test_db) -> TestClient:
    return TestClient(app)
