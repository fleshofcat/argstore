from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

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


async def test_get_db(mocker: MockerFixture, db_is_not_initialized):
    mocker.patch.object(
        database,
        "Settings",
        return_value=settings.Settings(
            sqlalchemy_database_url="sqlite+aiosqlite:///./test.db"
        ),
    )

    assert (database._engine, database._SessionFabric) == (None, None)

    sessions: list[AsyncSession] = []

    with patch("sqlalchemy.ext.asyncio.session.AsyncSession.close") as close_mock:

        async for session in database.get_db():
            sessions.append(session)
            assert session.is_active

        assert close_mock.called

    await sessions[0].close()
