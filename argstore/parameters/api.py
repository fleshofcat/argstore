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

    if read_user(db, user_name) is None:
        raise HTTPException(status_code=404, detail=f"User: '{user_name}' not found")

    param = schemas.CreateParameter(
        Name=param_name, Type=type_name, Value=value, Username=user_name
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
)
@router.get(
    "/{user_name}/{param_name}/",
    response_model=list[schemas.Parameter],
)
def read_parameter(
    response: Response,
    user_name: str,
    param_name: str,
    type_name: str | None = None,
    db: Session = Depends(get_db),
):
    if read_user(db, user_name):
        if params := crud.read_parameters(db, user_name, param_name, type_name):
            return params
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
            return []
    else:
        raise HTTPException(status_code=404, detail=f"User: '{user_name}' not found")


@router.delete("/{user_name}/{param_name}/{type_name}", status_code=204)
def delete_param(
    user_name: str,
    param_name: str,
    type_name: str,
    db: Session = Depends(get_db),
):
    if not crud.delete_parameter(
        db, user_name=user_name, param_name=param_name, type_name=type_name
    ):
        raise HTTPException(
            status_code=404,
            detail=f"Parameter: '{param_name}' "
            f"with user: '{user_name}' "
            f"and type: '{type_name}' not found",
        )


@router.get("/{username}", response_model=list[schemas.Parameter])
def read_all_user_parameters(username: str, db: Session = Depends(get_db)):
    if read_user(db, username):
        return crud.read_all_user_parameters(db, username)
    else:
        raise HTTPException(status_code=404, detail=f"User: '{username}' not found")
