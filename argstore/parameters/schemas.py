from pydantic import BaseModel, StrictInt, StrictStr, validator


class CreateParameter(BaseModel):
    name: StrictStr
    value: StrictStr | StrictInt

    @validator("name")
    def name_must_be_not_empty(cls, name):
        if name == "":
            raise ValueError("name must be not empty")
        return name


class Parameter(CreateParameter):
    id: int

    class Config:
        orm_mode = True
