from sqlalchemy.orm import Session

from argstore.users import models, schemas


def create_user(db: Session, user: schemas.CreateUser) -> models.User:
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_user(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.Name == username).first()


def read_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user: schemas.User) -> models.User | None:
    if (
        db.query(models.User).filter(models.User.Name == user.Name).update(user.dict())
        > 0
    ):
        db.commit()
        return read_user(db, user.Name)
    return None


def delete_user(db: Session, username: str) -> bool:
    if db.query(models.User).filter(models.User.Name == username).delete():
        db.commit()
        return True
    return False
