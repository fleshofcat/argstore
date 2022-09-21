import pytest
from pydantic import ValidationError

from argstore.parameters.schemas import JsonApiQueryMessage, Parameter


@pytest.mark.parametrize("name", ["string_name", "comb333name", "1234", "null"])
@pytest.mark.parametrize("typename, value", [("str", "some text"), ("int", "123")])
def test_parameter_schema(name, typename, value):
    Parameter(**{"Name": name, "Type": typename, "Value": value})


@pytest.mark.parametrize("bad_name", ["name with space", " ", "\t", "name\twith\ttab"])
def test_parameter_schema_name_validation(bad_name):
    with pytest.raises(ValidationError):
        Parameter(**{"Name": bad_name, "Type": "str", "Value": "val"})


@pytest.mark.parametrize("bad_type", ["float", " ", "\t", "123", "qwerty"])
def test_parameter_schema_type_validation(bad_type):
    with pytest.raises(ValidationError):
        Parameter(**{"Name": "name", "Type": bad_type, "Value": "val"})


@pytest.mark.parametrize(
    "bad_part",
    [
        {"Operation": ""},
        {"Operation": "."},
        {"Operation": " "},
        {"Operation": "unsupported_one"},
        {"Name": ""},
        {"Name": "name with space"},
        {"Name": " "},
        {"Name": "\t"},
        {"Name": "name\twith\ttab"},
        {"Type": ""},
        {"Type": " "},
        {"Type": "float"},
        {"Type": "int", "Value": "text"},
        {"Type": "int", "Value": ""},
        {"Type": "int", "Value": " "},
        {"Type": "int", "Value": "1.1"},
    ],
)
def test_JsonApiQueryMessage_validation(bad_part: dict):
    valid_json = {
        "Operation": "SetParam",
        "Name": "name",
        "Type": "str",
        "value": "1",
    }

    with pytest.raises(ValidationError):
        JsonApiQueryMessage(**{**valid_json, **bad_part})
