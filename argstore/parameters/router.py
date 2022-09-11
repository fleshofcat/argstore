from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from argstore.database import get_db
from argstore.parameters import crud, schemas
from argstore.parameters.crud import _cast_database_parameter_to_schema

router = APIRouter()


@router.post("/", response_model=schemas.Parameter, status_code=201)
async def create_parameter(
    param: schemas.CreateParameter, db: AsyncSession = Depends(get_db)
):
    return _cast_database_parameter_to_schema((await crud.create_parameter(db, param)))


@router.put("/", response_model=schemas.Parameter)
async def update_parameter(
    param: schemas.Parameter, db: AsyncSession = Depends(get_db)
):
    updated_param = await crud.update_parameter(db, param)
    if updated_param is None:
        raise HTTPException(status_code=404)
    return _cast_database_parameter_to_schema(updated_param)


@router.get("/", response_model=list[schemas.Parameter])
async def read_parameters(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return [
        _cast_database_parameter_to_schema(p)
        for p in (await crud.read_parameters(db, skip, limit))
    ]


@router.get("/{param_id}", response_model=schemas.Parameter)
async def read_parameter(param_id: int, db: AsyncSession = Depends(get_db)):
    db_param = await crud.read_parameter(db, param_id)
    if db_param is None:
        raise HTTPException(status_code=404)

    return _cast_database_parameter_to_schema(db_param)


@router.delete("/{param_id}", status_code=204)
async def delete_parameter(param_id: int, db: AsyncSession = Depends(get_db)):
    if not (await crud.delete_parameter(db, param_id)):
        raise HTTPException(status_code=404)
