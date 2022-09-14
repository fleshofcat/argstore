from sqlalchemy.orm import Session

from . import models, schemas

_possible_types = {"str": str, "int": int}


def create_parameter(db: Session, param: schemas.CreateParameter) -> models.Parameter:
    db_param = models.Parameter(param.dict())
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param


def read_parameters(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Parameter]:
    return db.query(models.Parameter).offset(skip).limit(limit).all()


def read_parameter(db: Session, param_id: int) -> models.Parameter | None:
    return db.query(models.Parameter).filter(models.Parameter.id == param_id).first()


def update_parameter(
    db: Session, param: schemas.CreateParameter
) -> models.Parameter | None:
    if (
        db.query(models.Parameter)
        .filter(models.Parameter.Name == param.Name)
        .filter(models.Parameter.Username == param.Username)
        .filter(models.Parameter.Type == param.Type)
        .update(param.dict())
        > 0
    ):
        db.commit()
        return (
            db.query(models.Parameter)
            .filter(models.Parameter.Name == param.Name)
            .filter(models.Parameter.Username == param.Username)
            .filter(models.Parameter.Type == param.Type)
            .first()
        )
    return None


def delete_parameter(db: Session, param_id: int) -> bool:
    if db.query(models.Parameter).filter(models.Parameter.id == param_id).delete():
        db.commit()
        return True
    return False
