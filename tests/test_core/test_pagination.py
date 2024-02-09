import pytest
from fastapi_pagination.bases import RawParams

from core.pagination import JSONAPIParams, JSONAPIPage


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


@pytest.mark.parametrize(
    "data, offset, limit, total, expected_page_size",
    [
        ([], 1, 10, 0, 0),  # Empty data
        (["item1", "item2"], 1, 10, 3, 2),  # Data with some items
        (["item1", "item2", "item3", "item4"], 2, 2, 4, 2),  # Offset and limit
        (["item1", "item2", "item2", "item3", "item4"], 2, 2, 5, 2),  # Offset and limit
    ],
)
def test_jsonapi_page_creation(data, offset, limit, total, expected_page_size):
    params = JSONAPIParams(offset=offset, limit=limit)
    page = JSONAPIPage.create(items=data, params=params, total=total)

    assert page.data == data[offset - 1 : offset - 1 + limit]
    assert len(page.data) == expected_page_size


def test_jsonapi_page_creation_missing_total():
    params = JSONAPIParams(offset=1, limit=10)
    data = ["item1", "item2"]

    with pytest.raises(AssertionError):
        JSONAPIPage.create(items=data, params=params)
