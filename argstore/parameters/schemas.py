from enum import Enum

from pydantic import BaseModel, StrictStr, validator


class SupportedType(str, Enum):
    str = "str"
    int = "int"


class Parameter(BaseModel):
    Name: StrictStr
    Type: SupportedType
    Value: str

    @validator("Name")
    def validate_name(cls, name: str):
        if name.strip() == "":
            raise ValueError("Name must be not empty")

        if "\t" in name or " " in name:
            raise ValueError("Name must not contain spaces or tabs")

        return name

    class Config:
        orm_mode = True


class CreateParameter(Parameter):
    Username: str
