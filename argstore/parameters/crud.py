from sqlalchemy.orm import Session

from argstore.parameters import models, schemas

_possible_types = {"str": str, "int": int}


def _cast_database_parameter_to_schema(param: models.Parameter) -> schemas.Parameter:
    return schemas.Parameter(
        id=param.id,
        name=param.name,
        value=_possible_types[param.type](param.value),
    )


def map_param_from_schema_to_model_dict(param: schemas.CreateParameter) -> dict:
    return dict(
        name=param.name, type=type(param.value).__name__, value=str(param.value)
    )


def create_parameter(db: Session, param: schemas.CreateParameter) -> models.Parameter:
    db_param = models.Parameter(**map_param_from_schema_to_model_dict(param))
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param


def read_parameter(db: Session, param_id: int) -> models.Parameter | None:
    return db.query(models.Parameter).filter(models.Parameter.id == param_id).first()


def read_parameters(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Parameter]:
    return db.query(models.Parameter).offset(skip).limit(limit).all()


def update_parameter(db: Session, param: schemas.Parameter) -> models.Parameter | None:
    if (
        db.query(models.Parameter)
        .filter(models.Parameter.id == param.id)
        .update(map_param_from_schema_to_model_dict(param))
        > 0
    ):
        db.commit()
        return read_parameter(db, param.id)
    return None


def delete_parameter(db: Session, param_id: int) -> bool:
    if db.query(models.Parameter).filter(models.Parameter.id == param_id).delete():
        db.commit()
        return True
    return False
