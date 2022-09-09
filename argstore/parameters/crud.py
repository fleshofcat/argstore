from sqlalchemy.orm import Session

from argstore.parameters import models, schemas


def create_parameter(db: Session, param: schemas.Parameter):
    db_param = models.Parameter(
        name=param.name, type=type(param.value).__name__, value=str(param.value)
    )
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param


def read_parameters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parameter).offset(skip).limit(limit).all()
