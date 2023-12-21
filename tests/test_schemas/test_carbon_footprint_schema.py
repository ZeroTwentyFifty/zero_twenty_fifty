from datetime import datetime

import pytest

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
        "referencePeriodStart": datetime(2023, 1, 1),
        "referencePeriodEnd": datetime(2023, 12, 31),
        "exemptedEmissionsPercent": 2.5,
        "exemptedEmissionsDescription": "Description of exempted emissions",
        "packagingEmissionsIncluded": True
    }

    return data


def test_carbon_footprint_schema_validation(valid_carbon_footprint_data):
    """Test successful validation for valid carbon footprint data."""
    footprint = CarbonFootprint(**valid_carbon_footprint_data)
    assert footprint.dict() == valid_carbon_footprint_data  # Assert all attributes are set correctly


def test_carbon_footprint_missing_declared_unit(valid_carbon_footprint_data):
    """Test validation error for missing declaredUnit."""
    invalid_data = valid_carbon_footprint_data.copy()
    del invalid_data["declaredUnit"]
    with pytest.raises(ValueError):
        CarbonFootprint(**invalid_data)


def test_carbon_footprint_invalid_exempted_emissions_percent(valid_carbon_footprint_data):
    """Test validation error for invalid exemptedEmissionsPercent."""
    invalid_data = valid_carbon_footprint_data.copy()
    invalid_data["exemptedEmissionsPercent"] = 6
    with pytest.raises(ValueError):
        CarbonFootprint(**invalid_data)


def test_carbon_footprint_invalid_data_types(valid_carbon_footprint_data):
    """Test validation errors for invalid data types."""
    invalid_data = valid_carbon_footprint_data.copy()
    invalid_data["declaredUnit"] = 10  # Should be a string
    invalid_data["referencePeriodStart"] = "invalid_date"  # Should be a datetime
    with pytest.raises(ValueError):
        CarbonFootprint(**invalid_data)
