from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..users.crud import read_user
from . import crud, schemas

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

    try:
        supported_types[type_name](value)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Support for type: {type_name} not found. "
            "supported types: 'str', 'int'",
        )
    except ValueError:
        raise HTTPException(
            status_code=422, detail=f"Type-value mismatch. {type_name=}, {value=}"
        )

    param = schemas.CreateParameter(
        Name=param_name, Type=type_name, Value=value, Username=user_name
    )

    if read_user(db, param.Username) is None:
        raise HTTPException(
            status_code=404, detail=f"User: '{param.Username}' not found"
        )
    if db_param := crud.update_parameter(db, param):
        response.status_code = status.HTTP_200_OK
        return db_param
    else:
        response.status_code = status.HTTP_201_CREATED
        return crud.create_parameter(db, param)


@router.get(
    "/{user_name}/{param_name}/{type_name}",
    response_model=list[schemas.Parameter],
    status_code=200,
)
@router.get(
    "/{user_name}/{param_name}/",
    response_model=list[schemas.Parameter],
)
def read_parameter(
    user_name: str,
    param_name: str,
    type_name: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.read_parameter(db, user_name, param_name, type_name)
