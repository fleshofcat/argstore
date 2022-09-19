from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from argstore import database, settings


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
