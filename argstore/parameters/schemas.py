from pydantic import BaseModel


class CreateParameter(BaseModel):
    name: str
    value: str | int


class Parameter(CreateParameter):
    id: int

    class Config:
        orm_mode = True
