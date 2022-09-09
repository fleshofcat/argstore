from pydantic import BaseModel


class Parameter(BaseModel):
    name: str
    value: str | int

    class Config:
        orm_mode = True
