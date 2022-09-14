import pytest

from argstore.parameters.schemas import Parameter


@pytest.mark.parametrize("name", ["string_name", "comb333name", "1234", "null"])
@pytest.mark.parametrize("typename", ["str", "int"])
@pytest.mark.parametrize("value", ["some text", "123"])
def test_parameter_schema(name, typename, value):
    Parameter(**{"Name": name, "Type": typename, "Value": value})
