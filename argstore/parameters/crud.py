from sqlalchemy.orm import Session

from argstore.parameters import models, schemas


def map_param_from_schema_to_model_dict(param: schemas.CreateParameter) -> dict:
    return dict(
        name=param.name, type=type(param.value).__name__, value=str(param.value)
    )


def create_parameter(db: Session, param: schemas.CreateParameter):
    db_param = models.Parameter(**map_param_from_schema_to_model_dict(param))
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param


def read_parameter(db: Session, param_id: int):
    return db.query(models.Parameter).filter(models.Parameter.id == param_id).first()


def read_parameters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parameter).offset(skip).limit(limit).all()
