from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from argstore import database, settings


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


def test_get_db(mocker: MockerFixture, db_is_not_initialized):
    mocker.patch.object(
        database,
        "Settings",
        return_value=settings.Settings(sqlalchemy_database_url="sqlite:///./test.db"),
    )

    session_generator = database.get_db()
    session: Session = next(session_generator)

    with patch.object(session, "close") as close_mock:
        with pytest.raises(StopIteration):
            next(session_generator)

        assert close_mock.called
    session.close()
