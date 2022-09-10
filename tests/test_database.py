from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from argstore.database import get_db


def test_get_db():
    session_generator = get_db()
    session: Session = next(session_generator)

    with patch.object(session, "close") as close_mock:
        with pytest.raises(StopIteration):
            next(session_generator)

        assert close_mock.called
    session.close()
