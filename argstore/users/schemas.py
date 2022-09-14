from pydantic import BaseModel

from ..parameters import schemas


class CreateUser(BaseModel):
    Name: str


class User(CreateUser):
    Parameters: list[schemas.Parameter]

    class Config:
        orm_mode = True
