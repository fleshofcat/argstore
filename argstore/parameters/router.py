from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from argstore.database import get_db
from argstore.parameters import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Parameter, status_code=201)
def create_parameter(param: schemas.CreateParameter, db: Session = Depends(get_db)):
    return crud.create_parameter(db, param)


@router.put("/", response_model=schemas.Parameter)
def update_parameter(param: schemas.CreateParameter, db: Session = Depends(get_db)):
    updated_param = crud.update_parameter(db, param)
    if updated_param is None:
        raise HTTPException(status_code=404)
    return updated_param


@router.get("/", response_model=list[schemas.Parameter])
def read_parameters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # return [p for p in crud.read_parameters(db, skip, limit)]
    return crud.read_parameters(db, skip, limit)


@router.get("/{param_id}", response_model=schemas.Parameter)
def read_parameter(param_id: int, db: Session = Depends(get_db)):
    db_param = crud.read_parameter(db, param_id)
    if db_param is None:
        raise HTTPException(status_code=404)

    return db_param


@router.delete("/{param_id}", status_code=204)
def delete_parameter(param_id: int, db: Session = Depends(get_db)):
    if not crud.delete_parameter(db, param_id):
        raise HTTPException(status_code=404)
