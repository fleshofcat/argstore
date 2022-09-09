from pydantic import BaseModel


class Parameter(BaseModel):
    id: int
    name: str
    value: str | int

    class Config:
        orm_mode = True
