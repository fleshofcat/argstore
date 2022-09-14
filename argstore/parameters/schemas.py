from pydantic import BaseModel, StrictStr, validator


class Parameter(BaseModel):
    Name: StrictStr
    Type: StrictStr
    Value: str

    @validator("Name")
    def validate_name(cls, name: str):
        if name.strip() == "":
            raise ValueError("Name must be not empty")

        if "\t" in name or " " in name:
            raise ValueError("Name must not contain spaces or tabs")

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
