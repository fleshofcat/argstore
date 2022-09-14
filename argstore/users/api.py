from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from . import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_users(db, skip, limit)


@router.get("/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
    if user := crud.read_user(db, username):
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User: '{username}' not found")


@router.delete("/{username}", status_code=204)
def delete_user(username: str, db: Session = Depends(get_db)):
    if not crud.delete_user(db, username):
        raise HTTPException(status_code=404, detail=f"User: '{username}' not found")
