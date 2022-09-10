from sqlalchemy import Column, Integer, String

from argstore.database import Base


class Parameter(Base):  # type: ignore
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    type = Column(String(10))
    value = Column(String)
