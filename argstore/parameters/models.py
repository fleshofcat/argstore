from sqlalchemy import Column, ForeignKey, Integer, String

from ..database import Base


class Parameter(Base):  # type: ignore
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    Name = Column(String(50))
    Type = Column(String(10))
    Value = Column(String)

    Username = Column(String(100), ForeignKey("users.Name"))
