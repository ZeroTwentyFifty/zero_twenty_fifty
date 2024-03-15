from datetime import datetime, timezone

import pytest

from db.repository.product_footprints import (
    create_new_product_footprint, retrieve_product_footprint, list_product_footprints,
    count_product_footprints
)
from schemas.product_footprint import ProductFootprint
from schemas.carbon_footprint import CarbonFootprint


@pytest.fixture(scope="module")
def valid_product_footprint_data(valid_carbon_footprint_data):
    data = {
        "id": "0c24b3eb-fb05-4353-ae08-a52ee051b392",
        "specVersion": "1.0.0",
        "version": 1,
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": None,
        "status": "Active",
        "companyName": "Test Company",
        "companyIds": [
            "urn:pathfinder:company:customcode:buyer-assigned:2874",
            "urn:pathfinder:company:customcode:vendor-assigned:5492"
        ],
        "productDescription": "Test Product",
        "productIds": [
            "urn:pathfinder:product:customcode:buyer-assigned:7329",
            "urn:pathfinder:product:customcode:vendor-assigned:2287",
            "urn:pathfinder: product:id: cas:50 - 00 - 0"
        ],
        "productCategoryCpc": "12345678",
        "productNameCompany": "Test Product by Test Company",
        "comment": "This was calculated very well.",
        "pcf": CarbonFootprint(**valid_carbon_footprint_data),  # Assuming a valid CarbonFootprint fixture
    }

    return data


@pytest.fixture(scope="module")
def invalid_product_footprint_data(valid_carbon_footprint_data):
    data = {
        "specVersion": "1.0.0",
        "version": -1,  # Invalid version (should be non-negative)
        "status": "In Progress",  # Invalid status
        "companyName": "Test Company",
        "companyIds": ["test-company-id-1", "test-company-id-2"],
        "productDescription": "Test Product",
        "productIds": ["test-product-id-1", "test-product-id-2"],
        "productCategoryCpc": "12345678",
        "productNameCompany": "Test Product by Test Company",
        "comment": "This was calculated very well.",
        "pcf": CarbonFootprint(**valid_carbon_footprint_data),
    }
    return data


@pytest.fixture(scope="module")
def two_product_footprints(valid_product_footprint_data, db_session):
    product_footprint_data1 = valid_product_footprint_data.copy()
    product_footprint_data1["id"] = "90163d8f-8465-4a6f-9e43-a58d68bef72f"
    product_footprint_data2 = valid_product_footprint_data.copy()
    product_footprint_data2["id"] = "80b79a90-0dbc-48d0-b910-551c09037d61"

    product_footprint_schema1 = ProductFootprint(**product_footprint_data1)
    product_footprint_schema2 = ProductFootprint(**product_footprint_data2)

    product_footprint1 = create_new_product_footprint(product_footprint_schema1, db_session)
    product_footprint2 = create_new_product_footprint(product_footprint_schema2, db_session)

    return product_footprint1, product_footprint2


def test_create_new_product_footprint(db_session, valid_product_footprint_data):
    product_footprint_schema = ProductFootprint(**valid_product_footprint_data)

    product_footprint = create_new_product_footprint(product_footprint_schema, db_session)
    assert product_footprint.companyName == "Test Company"
    assert product_footprint.productDescription == "Test Product"
    assert product_footprint.carbon_footprint.declared_unit == "kilogram"
    # TODO: Perform clean ups in a more structured way, this rollback exists in order
    #   to enable the `two_product_footprints` fixture to be used
    db_session.rollback()


# def test_create_new_product_footprint_database_error(db_session, valid_product_footprint_data):
#     """
#     TODO: This is a slightly useless test that doesn't do a whole lot, I left it in as I
#         wanted to show that the way our `create_new_product_footprint` repository function
#         works is a bit lame and could be flaky, ultimately we need to pick a level in the
#         request/response chain where we surface/handle exceptions, at the moment, (a relic
#         of the POC process), it's not clear where we handle these things. In a future
#         iteration, we need to provide more handling and be clearer about failure conditions.
#     Args:
#         db_session:
#         valid_product_footprint_data:
#
#     Returns:
#
#     """
#
#     product_footprint_schema = ProductFootprint(**valid_product_footprint_data)
#
#     # Mock database behavior to simulate an error
#     db_session.add = mock.MagicMock(side_effect=Exception("Simulated database error"))
#
#     with pytest.raises(Exception) as exc_info:
#         create_new_product_footprint(product_footprint_schema, db_session)
#
#     assert "Simulated database error" in str(exc_info.value)


def test_retrieve_product_footprint_not_found(db_session):
    item = retrieve_product_footprint("non-existent-id", db_session)
    assert item is None


def test_list_product_footprints_empty_returns_none(db_session):
    """
    Tests that `list_product_footprints` returns the correct number of results
    and that the data is as expected.
    """
    product_footprints = list_product_footprints(db_session)

    assert product_footprints is None


@pytest.mark.parametrize(
    "product_footprint_id",
    ["90163d8f-8465-4a6f-9e43-a58d68bef72f", "80b79a90-0dbc-48d0-b910-551c09037d61"])  # Extract IDs from fixture
def test_retrieve_product_footprint_success(db_session, product_footprint_id, two_product_footprints):
    retrieved_pf = retrieve_product_footprint(product_footprint_id, db_session)

    assert retrieved_pf is not None
    assert retrieved_pf.id == product_footprint_id


def test_list_product_footprints(two_product_footprints, db_session):
    """
    Tests that `list_product_footprints` returns the correct number of results
    and that the data is as expected.
    """
    product_footprints = list_product_footprints(db_session)

    assert len(product_footprints) == 2

    expected_ids = [
        "90163d8f-8465-4a6f-9e43-a58d68bef72f",
        "80b79a90-0dbc-48d0-b910-551c09037d61",
    ]
    for footprint in product_footprints:
        assert footprint.id in expected_ids
        assert footprint.specVersion == "1.0.0"


def test_count_product_footprints(two_product_footprints, db_session):
    expected_count = 2
    actual_count = count_product_footprints(db_session)

    assert actual_count == expected_count
