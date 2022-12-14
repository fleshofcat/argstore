from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def create_parameter(
    db: Session, param: schemas.CreateParameter
) -> List[models.Parameter]:
    db_param = models.Parameter(**param.dict())
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return [db_param]


def read_parameters(
    db: Session, user_name: str, param_name: str, type_name: Optional[str] = None
) -> List[models.Parameter]:
    query = (
        db.query(models.Parameter)
        .filter(models.Parameter.Name == param_name)
        .filter(models.Parameter.Username == user_name)
    )

    if type_name is not None:
        query = query.filter(models.Parameter.Type == type_name)

    return query.all()


def update_parameter(
    db: Session, param: schemas.CreateParameter
) -> List[models.Parameter]:
    if (
        db.query(models.Parameter)
        .filter(models.Parameter.Name == param.Name)
        .filter(models.Parameter.Username == param.Username)
        .filter(models.Parameter.Type == param.Type)
        .update(param.dict())
        > 0
    ):
        db.commit()
        return read_parameters(
            db, user_name=param.Username, param_name=param.Name, type_name=param.Type
        )
    return []


def delete_parameter(
    db: Session, user_name: str, param_name: str, type_name: str
) -> bool:

    if (
        db.query(models.Parameter)
        .filter(models.Parameter.Name == param_name)
        .filter(models.Parameter.Username == user_name)
        .filter(models.Parameter.Type == type_name)
        .delete()
    ):
        db.commit()
        return True
    return False


def read_all_user_parameters(
    db: Session,
    username: str,
) -> List[models.Parameter]:
    return (
        db.query(models.Parameter).filter(models.Parameter.Username == username).all()
    )
