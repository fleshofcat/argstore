from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from argstore.database import SessionLocal
from argstore.parameters import crud, models, schemas

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
        id=param.id,
        name=param.name,
        value=_possible_types[param.type](param.value),
    )


@router.post("/parameters", response_model=schemas.Parameter, status_code=201)
def create_parameter(param: schemas.CreateParameter, db: Session = Depends(get_db)):
    return _convert_database_parameter_to_schema(crud.create_parameter(db, param))


@router.get("/parameters", response_model=list[schemas.Parameter])
def get_parameters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return [
        _convert_database_parameter_to_schema(p)
        for p in crud.read_parameters(db, skip, limit)
    ]


@router.get("/parameters/{param_id}", response_model=schemas.Parameter)
def get_parameter(param_id: int, db: Session = Depends(get_db)):
    db_param = crud.read_parameter(db, param_id)
    if db_param is None:
        raise HTTPException(status_code=404, detail="Parameter not found")

    return _convert_database_parameter_to_schema(db_param)
