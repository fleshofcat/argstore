import typing
from enum import Enum
from pydoc import locate

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

    @validator("Value")
    def validate_type_value_compatibility(cls, value: str, values: dict):
        type_name = ""

        try:
            type_name = values["Type"].value
            CurrentType = typing.cast(typing.Type, locate(type_name))
            CurrentType(value)
        except (ValueError, KeyError):
            raise ValueError(f"Type-value mismatch. {type_name=}, {value=}")

        return value

    class Config:
        orm_mode = True


class CreateParameter(Parameter):
    Username: str


class JsonApiOperation(str, Enum):
    SetParam = "SetParam"


class JsonApiMessage(BaseModel):
    Operation: JsonApiOperation
    Name: StrictStr
    Type: SupportedType


class JsonApiQueryMessage(JsonApiMessage):
    Value: str

    @validator("Value")
    def validate_type_value_compatibility(cls, value: str, values: dict):
        type_name = ""

        try:
            type_name = values["Type"].value
            CurrentType = typing.cast(typing.Type, locate(type_name))
            CurrentType(value)
        except (ValueError, KeyError):
            raise ValueError(f"Type-value mismatch. {type_name=}, {value=}")

        return value


class Status(str, Enum):
    OK = ("OK",)
    ERROR = "ERROR"


class JsonApiResultMessage(JsonApiMessage):
    Status: Status


class JsonApiQuery(BaseModel):
    Query: list[JsonApiQueryMessage]


class JsonApiResult(BaseModel):
    Result: list[JsonApiResultMessage]
