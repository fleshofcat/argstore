from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from argstore import database


def test_get_db(mocker: MockerFixture):

    mocker.patch.object(database, "_engine")
    mocker.patch.object(database, "_SessionFabric")

    session_generator = database.get_db()
    session: Session = next(session_generator)

    with patch.object(session, "close") as close_mock:
        with pytest.raises(StopIteration):
            next(session_generator)

        assert close_mock.called
    session.close()
