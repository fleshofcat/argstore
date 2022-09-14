import pytest
from pydantic import ValidationError

from argstore.users.schemas import User


@pytest.mark.parametrize("bad_name", ["name with space", " ", "\t", "name\twith\ttab"])
def test_parameter_schema_name_validation(bad_name):
    with pytest.raises(ValidationError):
        User(**{"Name": bad_name, "Parameters": []})
