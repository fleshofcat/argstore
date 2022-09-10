from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from argstore.database import SessionLocal
from argstore.parameters import crud, schemas
from argstore.parameters.crud import _cast_database_parameter_to_schema

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Parameter, status_code=201)
def create_parameter(param: schemas.CreateParameter, db: Session = Depends(get_db)):
    return _cast_database_parameter_to_schema(crud.create_parameter(db, param))


@router.put("/", response_model=schemas.Parameter)
def update_parameter(param: schemas.Parameter, db: Session = Depends(get_db)):
    updated_param = crud.update_parameter(db, param)
    if updated_param is None:
        raise HTTPException(status_code=404)
    return _cast_database_parameter_to_schema(updated_param)


@router.get("/", response_model=list[schemas.Parameter])
def read_parameters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return [
        _cast_database_parameter_to_schema(p)
        for p in crud.read_parameters(db, skip, limit)
    ]


@router.get("/{param_id}", response_model=schemas.Parameter)
def read_parameter(param_id: int, db: Session = Depends(get_db)):
    db_param = crud.read_parameter(db, param_id)
    if db_param is None:
        raise HTTPException(status_code=404)

    return _cast_database_parameter_to_schema(db_param)


@router.delete("/{param_id}", status_code=204)
def delete_parameter(param_id: int, db: Session = Depends(get_db)):
    if not crud.delete_parameter(db, param_id):
        raise HTTPException(status_code=404)
