from datetime import datetime, timezone
import json

import pytest

from schemas.carbon_footprint import (
    CarbonFootprint, RegionOrSubregion, DeclaredUnit, BiogenicAccountingMethodology,
    CharacterizationFactors, CrossSectoralStandard
)


def test_carbon_footprint_schema_validation(valid_carbon_footprint_data):
    """Test successful validation for valid carbon footprint data."""
    footprint = CarbonFootprint(**valid_carbon_footprint_data)

    json_footprint_data = json.loads(footprint.model_dump_json())

    assert json_footprint_data["declaredUnit"] == "kilogram"
    assert json_footprint_data["unitaryProductAmount"] == 100
    assert json_footprint_data["pCfExcludingBiogenic"] == 10
    assert json_footprint_data["pCfIncludingBiogenic"] == 12
    assert json_footprint_data["fossilGhgEmissions"] == 8
    assert json_footprint_data["fossilCarbonContent"] == 5
    assert json_footprint_data["biogenicCarbonContent"] == 4
    assert json_footprint_data["dLucGhgEmissions"] == 2
    assert json_footprint_data["landManagementGhgEmissions"] == 3
    assert json_footprint_data["otherBiogenicGhgEmissions"] == 1
    assert json_footprint_data["iLucGhgEmissions"] == 2
    assert json_footprint_data["biogenicCarbonWithdrawal"] == -1
    assert json_footprint_data["aircraftGhgEmissions"] == 0.5
    assert json_footprint_data["characterizationFactors"] == "AR6"
    assert json_footprint_data["crossSectoralStandardsUsed"] == ["GHG Protocol Product standard"]
    assert json_footprint_data["productOrSectorSpecificRules"] == ["CFS Guidance for XYZ Sector"]
    assert json_footprint_data["biogenicAccountingMethodology"] == "PEF"
    assert json_footprint_data["boundaryProcessesDescription"] == "Description of boundary processes"
    assert json_footprint_data["referencePeriodStart"] == "2023-01-01T00:00:00+00:00"
    assert json_footprint_data["referencePeriodEnd"] == "2023-12-31T00:00:00+00:00"
    assert json_footprint_data["geographyCountrySubdivision"] == "AU"
    assert json_footprint_data["geographyCountry"] == "AU"
    assert json_footprint_data["geographyRegionOrSubregion"] == "Australia and New Zealand"
    assert json_footprint_data["secondaryEmissionFactorSources"] == [
        {
            "name": "ecoinvent",
            "version": "3.9.1"
        }
    ]
    assert json_footprint_data["exemptedEmissionsPercent"] == 2.5
    assert json_footprint_data["exemptedEmissionsDescription"] == "Description of exempted emissions"
    assert json_footprint_data["packagingEmissionsIncluded"] == True
    assert json_footprint_data["packagingGhgEmissions"] == 0.5
    assert json_footprint_data["allocationRulesDescription"] == "Description of allocation rules"
    assert json_footprint_data["uncertaintyAssessmentDescription"] == "Description of uncertainty assessment"
    assert json_footprint_data["primaryDataShare"] == 50
    assert json_footprint_data["dqi"] == {"key1": "value1", "key2": "value2"}
    assert json_footprint_data["assurance"] == {"key1": "value1", "key2": "value2"}


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


def test_region_or_subregion_values():
    assert RegionOrSubregion.AFRICA == 'Africa'
    assert RegionOrSubregion.AMERICAS == 'Americas'
    assert RegionOrSubregion.ASIA == 'Asia'
    assert RegionOrSubregion.EUROPE == 'Europe'
    assert RegionOrSubregion.OCEANIA == 'Oceania'
    assert RegionOrSubregion.AUSTRALIA_AND_NEW_ZEALAND == 'Australia and New Zealand'
    assert RegionOrSubregion.CENTRAL_ASIA == 'Central Asia'
    assert RegionOrSubregion.EASTERN_ASIA == 'Eastern Asia'
    assert RegionOrSubregion.EASTERN_EUROPE == 'Eastern Europe'
    assert RegionOrSubregion.LATIN_AMERICA_AND_THE_CARIBBEAN == 'Latin America and the Caribbean'
    assert RegionOrSubregion.MELANESIA == 'Melanesia'
    assert RegionOrSubregion.MICRONESIA == 'Micronesia'
    assert RegionOrSubregion.NORTHERN_AFRICA == 'Northern Africa'
    assert RegionOrSubregion.NORTHERN_AMERICA == 'Northern America'
    assert RegionOrSubregion.NORTHERN_EUROPE == 'Northern Europe'
    assert RegionOrSubregion.POLYNESIA == 'Polynesia'
    assert RegionOrSubregion.SOUTH_EASTERN_ASIA == 'South-eastern Asia'
    assert RegionOrSubregion.SOUTHERN_ASIA == 'Southern Asia'
    assert RegionOrSubregion.SOUTHERN_EUROPE == 'Southern Europe'
    assert RegionOrSubregion.SUB_SAHARAN_AFRICA == 'Sub-Saharan Africa'
    assert RegionOrSubregion.WESTERN_ASIA == 'Western Asia'
    assert RegionOrSubregion.WESTERN_EUROPE == 'Western Europe'


def test_declared_unit_values():
    assert DeclaredUnit.LITER == 'liter'
    assert DeclaredUnit.KILOGRAM == 'kilogram'
    assert DeclaredUnit.CUBIC_METER == 'cubic meter'
    assert DeclaredUnit.KILOWATT_HOUR == 'kilowatt hour'
    assert DeclaredUnit.MEGAJOULE == 'megajoule'
    assert DeclaredUnit.TON_KILOMETER == 'ton kilometer'
    assert DeclaredUnit.SQUARE_METER == 'square meter'


def test_biogenic_accounting_methodology_values():
    assert BiogenicAccountingMethodology.PEF.value == 'PEF'
    assert BiogenicAccountingMethodology.ISO.value == 'ISO'
    assert BiogenicAccountingMethodology.GHGP.value == 'GHGP'
    assert BiogenicAccountingMethodology.QUANTIS.value == 'Quantis'

    with pytest.raises(AttributeError):
        assert BiogenicAccountingMethodology.Invalid


def test_characterization_factors_values():
    assert CharacterizationFactors.AR5 == 'AR5'
    assert CharacterizationFactors.AR6 == 'AR6'

    with pytest.raises(AttributeError):
        assert CharacterizationFactors.Invalid


def test_cross_sectoral_standard_values():
    assert CrossSectoralStandard.GHG_PROTOCOL == 'GHG Protocol Product standard'
    assert CrossSectoralStandard.ISO_14067 == 'ISO Standard 14067'
    assert CrossSectoralStandard.ISO_14044 == 'ISO Standard 14044'
