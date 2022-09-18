from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..database import get_db
from ..users.crud import read_user
from . import crud, schemas
from .schemas import SupportedType

router = APIRouter()


@router.post(
    "/{user_name}/{param_name}/{type_name}",
    response_model=list[schemas.Parameter],
)
def set_parameter(
    user_name: str,
    param_name: str,
    type_name: SupportedType,
    response: Response,
    value: str = Body(media_type="text/plain"),
    db: Session = Depends(get_db),
):
    try:
        assert read_user(db, user_name), f"User: '{user_name}' not found"
        param = schemas.CreateParameter(
            Name=param_name,
            Type=type_name,
            Value=value,
            Username=user_name,
        )

        if db_param := crud.update_parameter(db, param):
            response.status_code = status.HTTP_200_OK
            return db_param
        else:
            response.status_code = status.HTTP_201_CREATED
            return crud.create_parameter(db, param)

    except AssertionError as err:
        raise HTTPException(status_code=404, detail=str(err))

    except ValidationError as err:
        raise HTTPException(status_code=422, detail=str(err))


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
    type_name: SupportedType | None = None,
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
    type_name: SupportedType,
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


json_api_router = APIRouter()


@json_api_router.post("/{user_name}", response_model=schemas.JsonApiResult)
def set_parameter_with_json_api(
    user_name: str,
    query: schemas.JsonApiQuery,
    response: Response,
    db: Session = Depends(get_db),
):
    user_exists = bool(read_user(db, user_name))

    if not user_exists:
        response.status_code = status.HTTP_404_NOT_FOUND

    result = schemas.JsonApiResult(Result=[])

    for q in query.Query:
        param = schemas.CreateParameter(
            Name=q.Name,
            Type=q.Type,
            Value=q.Value,
            Username=user_name,
        )

        result_status = schemas.Status.ERROR

        if user_exists:
            if crud.update_parameter(db, param):
                result_status = schemas.Status.OK
            elif crud.create_parameter(db, param):
                result_status = schemas.Status.OK

        result.Result += [
            schemas.JsonApiResultMessage(
                Operation=q.Operation, Name=q.Name, Type=q.Type, Status=result_status
            )
        ]

    return result
