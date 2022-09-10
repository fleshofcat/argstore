from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from argstore.settings import Settings

Base = declarative_base()


_SessionFabric = None
_engine = None


def create_db_engine(sqlalchemy_database_url: str = "") -> Engine:
    global _engine
    if not _engine:
        if not sqlalchemy_database_url:
            sqlalchemy_database_url = Settings().sqlalchemy_database_url

        _engine = create_engine(
            sqlalchemy_database_url, connect_args={"check_same_thread": False}
        )
    return _engine


def create_session() -> Session:
    global _SessionFabric
    if not _SessionFabric:
        _SessionFabric = sessionmaker(
            autocommit=False, autoflush=False, bind=create_db_engine()
        )

    return _SessionFabric()


def get_db() -> Generator:
    db: Session = create_session()
    try:
        yield db
    finally:
        db.close()
