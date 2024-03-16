from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from db.models.product_footprint import ProductFootprint, ProductFootprintStatus
from db.models.carbon_footprint import CarbonFootprintModel, ProductOrSectorSpecificRuleModel, EmissionFactorDatasetModel
from schemas.carbon_footprint import (
    CharacterizationFactors, BiogenicAccountingMethodology, DeclaredUnit, RegionOrSubregion,
    ProductOrSectorSpecificRuleOperator
)


def test_product_footprint_creation(db_session):

    product_footprint = ProductFootprint(
        id="test_id",
        precedingPfIds=["prior-id"],
        specVersion="1.0",
        version=1,
        created=datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat(),
        updated=datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat(),
        status="ACTIVE",
        statusComment="",
        validityPeriodStart=datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat(),
        validityPeriodEnd=datetime(2026, 1, 1, tzinfo=timezone.utc).isoformat(),
        companyName="Test Company",
        companyIds=[],
        productDescription="Test Product",
        productIds=[],
        productCategoryCpc="Test Category",
        productNameCompany="Test Product Name",
        comment="Test Comment",
        carbon_footprint=CarbonFootprintModel(
            declared_unit=DeclaredUnit.KILOGRAM,
            unitary_product_amount=1.5,
            pcf_excluding_biogenic=2.3,
            pcf_including_biogenic=3.0,
            fossil_ghg_emissions=1.8,
            fossil_carbon_content=1.2,
            biogenic_carbon_content=0.5,
            dluc_ghg_emissions=0.2,
            land_management_ghg_emissions=0.1,
            other_biogenic_ghg_emissions=0.4,
            iluc_ghg_emissions=0.6,
            biogenic_carbon_withdrawal=0.3,
            aircraft_ghg_emissions=0.8,
            characterization_factors=CharacterizationFactors.AR6,
            cross_sectoral_standards_used=["ISO Standard 14044", "ISO Standard 14067"],
            product_or_sector_specific_rules=[
                ProductOrSectorSpecificRuleModel(
                    operator=ProductOrSectorSpecificRuleOperator.OTHER,
                    rule_names=["Rule1", "Rule2"],
                    other_operator_name="Custom Operator"
                )
            ],
            biogenic_accounting_methodology=BiogenicAccountingMethodology.PEF,
            boundary_processes_description="Cradle-to-gate",
            reference_period_start=datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat(),
            reference_period_end=datetime(2023, 12, 31, tzinfo=timezone.utc).isoformat(),
            geography_region_or_subregion=RegionOrSubregion.ASIA,
            secondary_emission_factor_sources=[
                EmissionFactorDatasetModel(
                    name="ecoinvent",
                    version="1.2.3"
                ),
                EmissionFactorDatasetModel(
                    name="internal database",
                    version="3.2.1"
                )
            ],
            exempted_emissions_percent=2.5,
            exempted_emissions_description="Emissions from transport excluded",
            packaging_emissions_included=True,
            packaging_ghg_emissions=0.15,
            allocation_rules_description="Allocation based on mass",
            uncertainty_assessment_description="Monte Carlo simulation",
            primary_data_share=0.6,
            dqi={},
            assurance={}
        ),
        extensions={}
    )

    db_session.add(product_footprint)
    db_session.commit()

    item = db_session.query(ProductFootprint).filter(ProductFootprint.id == 'test_id').first()
    assert item.id == "test_id"
    assert item.specVersion == "1.0"
    assert item.version == 1
    assert item.created.isoformat() == '2023-01-01T00:00:00+00:00'
    # assert product_footprint.status == ProductFootprintStatus.ACTIVE
    # assert product_footprint.companyName == "Test Company"
    # assert product_footprint.companyIds == []
    # assert product_footprint.productDescription == "Test Product"
    # assert product_footprint.productIds == []
    # assert product_footprint.productCategoryCpc == "Test Category"
    # assert product_footprint.productNameCompany == "Test Product Name"
    # assert product_footprint.comment == "Test Comment"
    assert isinstance(item.carbon_footprint, CarbonFootprintModel)


def test_product_footprint_status_values():
    assert ProductFootprintStatus.ACTIVE.value == "Active"
    assert ProductFootprintStatus.DEPRECATED.value == "Deprecated"


def test_product_footprint_id_field_is_unique(db_session):
    # Create a record
    record1 = ProductFootprint(
        id="test_for_uniqueness",
        comment="test"
    )
    db_session.add(record1)
    db_session.commit()

    # Attempt to create another record with the same id
    record2 = ProductFootprint(
        id="test_for_uniqueness",
        comment = "test"
    )
    db_session.add(record2)
    with pytest.raises(IntegrityError, match="duplicate key value violates unique constraint"):
        db_session.commit()
