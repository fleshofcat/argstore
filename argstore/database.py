from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from argstore.settings import Settings

Base = declarative_base()

_db_url = ""


def set_sqlalchemy_database_url(url: str):
    global _db_url
    _db_url = url


_SessionFabric = None
_engine = None


def create_db_engine() -> AsyncEngine:
    global _engine
    if not _engine:
        if not _db_url:
            set_sqlalchemy_database_url(Settings().sqlalchemy_database_url)

        _engine = create_async_engine(
            _db_url, connect_args={"check_same_thread": False}, echo=True
        )
    return _engine


async def get_db():
    global _SessionFabric
    if not _SessionFabric:
        _SessionFabric = sessionmaker(
            expire_on_commit=False, class_=AsyncSession, bind=create_db_engine()
        )

    session: AsyncSession = _SessionFabric()
    try:
        yield session
    finally:
        await session.close()
