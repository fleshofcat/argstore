from typing import List

from pydantic import BaseModel, validator

from ..parameters import schemas


class CreateUser(BaseModel):
    Name: str

    @validator("Name")
    def validate_name(cls, name: str):
        if name.strip() == "":
            raise ValueError("Name must be not empty")

        if "\t" in name or " " in name:
            raise ValueError("Name must not contain spaces or tabs")

        return name


class User(CreateUser):
    Parameters: List[schemas.Parameter]

    class Config:
        orm_mode = True
