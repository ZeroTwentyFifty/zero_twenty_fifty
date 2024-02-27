import pytest
from pydantic import BaseModel, ValidationError


from schemas.base_types import NonEmptyString


def test_non_empty_string_valid():
    class Model(BaseModel):
        value: NonEmptyString

    Model(value="hello")


def test_non_empty_string_empty():
    class Model(BaseModel):
        value: NonEmptyString

    with pytest.raises(ValidationError) as excinfo:
        Model(value="")

    assert excinfo.value.errors()[0]["loc"] == ("value",)
    assert excinfo.value.errors()[0]["msg"] == "String should have at least 1 character"
