from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


_possible_types = {"str": str, "int": int}


def _convert_database_parameter_to_schema(param: models.Parameter) -> schemas.Parameter:
    return schemas.Parameter(
        name=param.name,
        value=_possible_types[param.type](param.value),
    )


@router.post("/parameters", response_model=schemas.Parameter)
def create_parameter(param: schemas.Parameter, db: Session = Depends(get_db)):
    return _convert_database_parameter_to_schema(crud.create_parameter(db, param))
