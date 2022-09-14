from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from argstore.database import get_db
from argstore.parameters import crud, models, schemas
from argstore.users.models import User

router = APIRouter()


@router.post(
    "/{user_name}/{param_name}/{type_name}",
    response_model=list[schemas.Parameter],
)
def set_parameter(
    user_name: str,
    param_name: str,
    type_name: str,
    response: Response,
    value: str = Body(media_type="text/plain"),
    db: Session = Depends(get_db),
):
    supported_types = {"str": str, "int": int}

    if type_name not in supported_types:
        raise HTTPException(
            status_code=404,
            detail=f"Support for type: {type_name} not found. "
            "supported types: 'str', 'int'",
        )

    try:
        supported_types[type_name](value)
    except ValueError:
        raise HTTPException(
            status_code=422, detail=f"Type-value mismatch. {type_name=}, {value=}"
        )

    param = schemas.CreateParameter(
        Name=param_name, Type=type_name, Value=value, Username=user_name
    )

    # TODO Move it to users/crud.py
    if db.query(User).where(User.Name == param.Username).first() is None:
        raise HTTPException(
            status_code=404, detail=f"User: '{param.Username}' not found"
        )

    updated_rows = (
        db.query(models.Parameter)
        .filter(models.Parameter.Name == param.Name)
        .filter(models.Parameter.Username == param.Username)
        .filter(models.Parameter.Type == param.Type)
        .update(param.dict())
    )

    if updated_rows > 0:
        response.status_code = status.HTTP_200_OK
        db_param = (
            db.query(models.Parameter)
            .filter(models.Parameter.Name == param_name)
            .filter(models.Parameter.Username == user_name)
            .filter(models.Parameter.Type == type_name)
            .first()
        )
    else:
        response.status_code = status.HTTP_201_CREATED
        return [crud.create_parameter(db, param)]

    db.commit()
    db.refresh(db_param)
    return [db_param]


@router.get(
    "/{user_name}/{param_name}/{type_name}",
    response_model=list[schemas.Parameter],
    status_code=200,
)
def read_parameter(
    user_name: str,
    param_name: str,
    type_name: str,
    db: Session = Depends(get_db),
):
    db_param = (
        db.query(models.Parameter)
        .filter(models.Parameter.Name == param_name)
        .filter(models.Parameter.Username == user_name)
        .filter(models.Parameter.Type == type_name)
        .first()
    )
    if db_param is None:
        raise HTTPException(
            status_code=404, detail=f"Parameter: '{param_name}' not found"
        )

    return [db_param]
