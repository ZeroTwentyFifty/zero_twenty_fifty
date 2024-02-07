import pytest
from fastapi_pagination.bases import RawParams

from core.pagination import JSONAPIParams


def test_jsonapi_params_valid():
    params = JSONAPIParams(offset=2, limit=20)
    assert params.offset == 2
    assert params.limit == 20
    assert params.to_raw_params() == RawParams(limit=20, offset=2)


def test_jsonapi_params_invalid_offset_too_low():
    with pytest.raises(ValueError):
        JSONAPIParams(offset=0, limit=10)


def test_jsonapi_params_invalid_limit_too_small():
    with pytest.raises(ValueError):
        JSONAPIParams(offset=1, limit=-1)


def test_jsonapi_params_invalid_limit_too_large():
    with pytest.raises(ValueError):
        JSONAPIParams(offset=1, limit=101)


def test_jsonapi_params_default_values():
    params = JSONAPIParams()
    assert params.offset == 1
    assert params.limit == 10
