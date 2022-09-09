from sqlalchemy.orm import Session

from . import models, schemas


def create_parameter(db: Session, param: schemas.Parameter):
    db_param = models.Parameter(
        name=param.name, type=type(param.value).__name__, value=str(param.value)
    )
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param
