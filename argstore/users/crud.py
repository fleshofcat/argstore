from typing import List, Optional

from sqlalchemy.orm import Session

from argstore.users import models, schemas


def create_user(db: Session, user: schemas.CreateUser) -> models.User:
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_user(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.Name == username).first()


def read_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, username: str) -> bool:
    if db.query(models.User).filter(models.User.Name == username).delete():
        db.commit()
        return True
    return False
