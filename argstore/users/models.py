from sqlalchemy import Column, String
from sqlalchemy.orm import RelationshipProperty, relationship

from ..database import Base


class User(Base):  # type: ignore
    __tablename__ = "users"

    Name = Column(String(100), primary_key=True, index=True, unique=True)

    Parameters: RelationshipProperty = relationship("Parameter", back_populates="User")
