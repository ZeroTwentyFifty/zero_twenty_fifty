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
    "data, offset, limit, total, expected_page_size, expected_page_data",
    [
        ([], 1, 10, 0, 0, []),  # Empty data
        (["item1", "item2"], 1, 10, 3, 2, ["item1", "item2"]),  # Data with some items
        (["item1", "item2", "item3", "item4"], 2, 2, 4, 2, ["item2", "item3"]),  # Offset and limit
        (["item1", "item2", "item2", "item3", "item4"], 2, 2, 5, 2, ["item2", "item2"])  # Offset and limit
    ],
)
def test_jsonapi_page_creation(data, offset, limit, total, expected_page_size, expected_page_data):
    params = JSONAPIParams(offset=offset, limit=limit)
    page = JSONAPIPage.create(items=data, params=params, total=total)

    assert page.data == expected_page_data
    assert len(page.data) == expected_page_size


def test_jsonapi_page_creation_missing_total():
    params = JSONAPIParams(offset=1, limit=10)
    data = ["item1", "item2"]

    with pytest.raises(AssertionError):
        JSONAPIPage.create(items=data, params=params)


def test_jsonapi_page_creation_with_empty_data():
    params = JSONAPIParams(offset=1, limit=10)
    data = []
    total = 0

    page = JSONAPIPage.create(items=data, params=params, total=total)

    assert page.data == []
    assert len(page.data) == 0


def test_jsonapi_page_creation_with_limit_greater_than_total():
    params = JSONAPIParams(offset=1, limit=10)
    data = ["item1", "item2", "item3"]
    total = 3

    page = JSONAPIPage.create(items=data, params=params, total=total)

    assert page.data == data
    assert len(page.data) == total


def test_get_page_data(app):
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    params = JSONAPIParams(offset=2, limit=3)

    page_data = JSONAPIPage._get_page_data(items=items, params=params)

    assert len(page_data) == 3
    assert page_data == [2, 3, 4]
