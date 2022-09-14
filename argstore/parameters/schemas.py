from pydantic import BaseModel, StrictStr, validator


class Parameter(BaseModel):
    Name: StrictStr
    Type: StrictStr
    Value: str

    @validator("Name")
    def name_must_be_not_empty(cls, name):
        if name == "":
            raise ValueError("Name must be not empty")
        return name

    @validator("Type")
    def type_mast_be_str_or_int(cls, type_name):
        if type_name not in ("str", "int"):
            raise ValueError(f"Type mast be 'str' or 'int', got '{type_name}' instead")
        return type_name

    class Config:
        orm_mode = True


class CreateParameter(Parameter):
    Username: str
