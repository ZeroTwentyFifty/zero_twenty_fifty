from datetime import datetime
from unittest import mock

import pytest
import sqlalchemy
import pydantic

#from db.models.product_footprint import ProductFootprint
from db.repository.product_footprints import create_new_product_footprint, retrieve_product_footprint
from schemas.product_footprint import ProductFootprint
from schemas.carbon_footprint import CarbonFootprint


@pytest.fixture(scope="function")
def valid_carbon_footprint_data():
    data = {
        "declaredUnit": "kgCO2e/kg",
        "unitaryProductAmount": 100,
        "pCfExcludingBiogenic": 10,
        "pCfIncludingBiogenic": 12,
        "fossilGhgEmissions": 8,
        "fossilCarbonContent": 5,
        "biogenicCarbonContent": 4,
        "characterizationFactors": "IPCC 2013",
        "crossSectoralStandardsUsed": ["PAS 2050"],
        "productOrSectorSpecificRules": ["CFS Guidance for XYZ Sector"],
        "boundaryProcessesDescription": "Description of boundary processes",
        "referencePeriodStart": datetime(2023, 1, 1).isoformat(),
        "referencePeriodEnd": datetime(2023, 12, 31).isoformat(),
        "exemptedEmissionsPercent": 2.5,
        "exemptedEmissionsDescription": "Description of exempted emissions",
        "packagingEmissionsIncluded": True
    }

    return data


@pytest.fixture(scope="function")
def valid_product_footprint_data(valid_carbon_footprint_data):
    data = {
        "specVersion": "1.0.0",
        "version": 1,
        "status": "Active",
        "companyName": "Test Company",
        "companyIds": ["test-company-id-1", "test-company-id-2"],
        "productDescription": "Test Product",
        "productIds": ["test-product-id-1", "test-product-id-2"],
        "productCategoryCpc": "12345678",
        "productNameCompany": "Test Product by Test Company",
        "comment": "This was calculated very well.",
        "pcf": CarbonFootprint(**valid_carbon_footprint_data),  # Assuming a valid CarbonFootprint fixture
    }

    return data


@pytest.fixture(scope="function")
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


def test_create_new_product_footprint(db_session, valid_product_footprint_data):
    product_footprint_schema = ProductFootprint(**valid_product_footprint_data)

    product_footprint = create_new_product_footprint(product_footprint_schema, db_session)
    assert product_footprint.companyName == "Test Company"
    assert product_footprint.productDescription == "Test Product"
    assert product_footprint.pcf['declaredUnit'] == "kgCO2e/kg"


def test_create_new_product_footprint_database_error(db_session, valid_product_footprint_data):
    """
    TODO: This is a slightly useless test that doesn't do a whole lot, I left it in as I
        wanted to show that the way our `create_new_product_footprint` repository function
        works is a bit lame and could be flaky, ultimately we need to pick a level in the
        request/response chain where we surface/handle exceptions, at the moment, (a relic
        of the POC process), it's not clear where we handle these things. In a future
        iteration, we need to provide more handling and be clearer about failure conditions.
    Args:
        db_session:
        valid_product_footprint_data:

    Returns:

    """

    product_footprint_schema = ProductFootprint(**valid_product_footprint_data)

    # Mock database behavior to simulate an error
    db_session.add = mock.MagicMock(side_effect=Exception("Simulated database error"))

    with pytest.raises(Exception) as exc_info:
        create_new_product_footprint(product_footprint_schema, db_session)

    assert "Simulated database error" in str(exc_info.value)


def test_retrieve_product_footprint_not_found(db_session):
    item = retrieve_product_footprint("non-existent-id", db_session)
    assert item is None


"""
@pytest.fixture(scope="function")
def valid_product_footprint_data(valid_carbon_footprint_data):
    data = {
        "specVersion": "1.0.0",
        "version": 1,
        "status": "Active",
        "companyName": "Test Company",
        # ... rest of the data
    }
    return data

@pytest.fixture(scope="function")
def product_footprints(db_session: Session, valid_product_footprint_data):
    pf1 = ProductFootprint(id=uuid4(), **valid_product_footprint_data)
    pf2 = ProductFootprint(id=uuid4(), **valid_product_footprint_data)
    db_session.add_all([pf1, pf2])
    db_session.commit()
    return [pf1, pf2]  # Return a list of ProductFootprint objects

@pytest.mark.parametrize("product_footprint_id", [pf.id for pf in product_footprints])  # Extract IDs from fixture
def test_retrieve_product_footprint_success(db_session: Session, product_footprints: list[ProductFootprint], product_footprint_id):
    retrieved_pf = retrieve_product_footprint(str(product_footprint_id), db_session)

    assert retrieved_pf is not None
    assert retrieved_pf.id == product_footprint_id
    # ... more specific field assertions
"""