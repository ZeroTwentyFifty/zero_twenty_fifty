import pytest

from datetime import datetime
from uuid import UUID

from schemas.carbon_footprint import CarbonFootprint
from schemas.product_footprint import ProductFootprint


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


def test_product_footprint_schema_validation(valid_product_footprint_data):
    """Test successful validation for valid product footprint data."""
    footprint = ProductFootprint(**valid_product_footprint_data)
    # Assert key attributes to ensure model creation and default values
    assert isinstance(footprint.id, UUID)
    assert footprint.specVersion == "1.0.0"
    assert footprint.companyName == "Test Company"
    assert footprint.pcf.declaredUnit == "kgCO2e/kg"  # Example assertion for nested model


def test_product_footprint_missing_version(valid_product_footprint_data):
    """Test validation error for missing version."""
    invalid_data = valid_product_footprint_data.copy()
    del invalid_data["version"]
    with pytest.raises(ValueError):
        ProductFootprint(**invalid_data)


def test_product_footprint_invalid_status(valid_product_footprint_data):
    """Test validation error for invalid status."""
    invalid_data = valid_product_footprint_data.copy()
    invalid_data["status"] = "InvalidStatus"
    with pytest.raises(ValueError):
        ProductFootprint(**invalid_data)


def test_product_footprint_invalid_version_range(valid_product_footprint_data):
    """Test validation error for version outside valid range."""
    invalid_data = valid_product_footprint_data.copy()
    invalid_data["version"] = 2**31
    with pytest.raises(ValueError):
        ProductFootprint(**invalid_data)


# def test_product_footprint_orm_mode(valid_product_footprint_data):
#     """Test ORM mode for ProductFootprint model."""
#     # Assuming a hypothetical ProductFootprintORM model with the same attributes
#     product_orm = ProductFootprintORM(**valid_product_footprint_data)
#     footprint = ProductFootprint.from_orm(product_orm)
#     assert footprint.dict() == product_orm.__dict__  # Assuming similar attribute names