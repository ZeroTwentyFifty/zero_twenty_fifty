import pytest
from pydantic import ValidationError

from schemas.carbon_footprint import EmissionFactorDS


def test_emission_factor_valid():
    data = {
        "name": "ecoinvent",
        "version": "2.3.0"
    }
    emission_factor_ds = EmissionFactorDS(**data)

    assert emission_factor_ds.name == "ecoinvent"
    assert emission_factor_ds.version == "2.3.0"


def test_emission_factor_missing_name():
    data = {
        "version": "1.0.0"
    }
    with pytest.raises(ValidationError):
        EmissionFactorDS(**data)


def test_emission_factor_empty_version():
    data = {
        "name": "ecoinvent",
        "version": ""
    }
    with pytest.raises(ValidationError):
        EmissionFactorDS(**data)


def test_emission_factor_ds_json_representation():
    data = {
        "name": "ecoinvent",
        "version": "3.9.1"
    }
    emission_factor_ds = EmissionFactorDS(**data)

    expected_json = '{"name":"ecoinvent","version":"3.9.1"}'
    assert emission_factor_ds.model_dump_json() == expected_json


# def test_emission_factor_ds_json_representation():
#     emission_factor_ds = EmissionFactorDS(name="ecoinvent", version="3.9.1")
#     expected_json = '{"name":"ecoinvent","version":"3.9.1"}'
#
#     assert emission_factor_ds.model_dump_json() == expected_json
#
#     # Additionally, ensure the dict representation is as expected using .dict()
#     assert emission_factor_ds.model_dump() == {"name": "ecoinvent", "version": "3.9.1"}
