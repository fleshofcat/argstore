import pytest
from pydantic import ValidationError

from argstore.parameters.schemas import Parameter


@pytest.mark.parametrize("name", ["string_name", "comb333name", "1234", "null"])
@pytest.mark.parametrize("typename", ["str", "int"])
@pytest.mark.parametrize("value", ["some text", "123"])
def test_parameter_schema(name, typename, value):
    Parameter(**{"Name": name, "Type": typename, "Value": value})


@pytest.mark.parametrize("bad_name", ["name with space", " ", "\t", "name\twith\ttab"])
def test_parameter_schema_name_validation(bad_name):
    with pytest.raises(ValidationError):
        Parameter(**{"Name": bad_name, "Type": "str", "Value": "val"})
