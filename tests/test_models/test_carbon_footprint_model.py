from datetime import datetime, timezone

from db.models.carbon_footprint import (
    CarbonFootprintModel, ProductOrSectorSpecificRuleModel, EmissionFactorDatasetModel
)
from schemas.carbon_footprint import (
    CharacterizationFactors, BiogenicAccountingMethodology, DeclaredUnit, RegionOrSubregion,
    ProductOrSectorSpecificRuleOperator
)


def test_carbon_footprint_creation(db_session):

    carbon_footprint = CarbonFootprintModel(
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
        cross_sectoral_standards_used="ISO 14040, ISO 14067",  # Example with multiple values
        product_or_sector_specific_rules=[
            ProductOrSectorSpecificRuleModel(
                operator=ProductOrSectorSpecificRuleOperator.PEF,
                rule_names=["Rule 1", "Rule 2"],
                other_operator_name=None
            ),
            ProductOrSectorSpecificRuleModel(
                operator=ProductOrSectorSpecificRuleOperator.OTHER,
                rule_names=["Rule 1", "Rule 2"],
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
    )
    db_session.add(carbon_footprint)
    db_session.commit()

    assert carbon_footprint.pk is not None
