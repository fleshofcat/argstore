from pydantic import BaseModel, StrictStr


class CreateParameter(BaseModel):
    name: str
    value: StrictStr | int


class Parameter(CreateParameter):
    id: int

    class Config:
        orm_mode = True
