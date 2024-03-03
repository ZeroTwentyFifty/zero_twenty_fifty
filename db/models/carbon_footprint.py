from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from schemas.carbon_footprint import (
    CharacterizationFactors, BiogenicAccountingMethodology, DeclaredUnit, RegionOrSubregion,
    ProductOrSectorSpecificRuleOperator
)


class ProductOrSectorSpecificRuleModel(Base):
    __tablename__ = "productorsectorspecificrule"

    pk = Column(Integer, primary_key=True, autoincrement=True)
    operator = Column(Enum(ProductOrSectorSpecificRuleOperator), nullable=False)
    rule_names = Column(ARRAY(String), nullable=False)
    other_operator_name = Column(String, nullable=True)

    carbon_footprint_pk = Column(Integer, ForeignKey('carbonfootprint.pk'))
    carbon_footprint = relationship(
        "CarbonFootprintModel", back_populates="product_or_sector_specific_rules", uselist=True
    )


class EmissionFactorDatasetModel(Base):
    __tablename__ = "emissionfactordataset"

    pk = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)

    carbon_footprint_pk = Column(Integer, ForeignKey('carbonfootprint.pk'))
    carbon_footprint = relationship(
        "CarbonFootprintModel", back_populates="secondary_emission_factor_sources", uselist=True
    )

class CarbonFootprintModel(Base):
    __tablename__ = "carbonfootprint"

    pk = Column(Integer, primary_key=True, autoincrement=True)
    declared_unit = Column(Enum(DeclaredUnit))
    unitary_product_amount = Column(Float, CheckConstraint('unitary_product_amount > 0'))
    pcf_excluding_biogenic = Column(Float, nullable=False)
    pcf_including_biogenic = Column(Float)
    fossil_ghg_emissions = Column(Float, nullable=False)
    fossil_carbon_content = Column(Float, nullable=False)
    biogenic_carbon_content = Column(Float, nullable=False)
    dluc_ghg_emissions = Column(Float)
    land_management_ghg_emissions = Column(Float)
    other_biogenic_ghg_emissions = Column(Float)
    iluc_ghg_emissions = Column(Float)
    biogenic_carbon_withdrawal = Column(Float)
    aircraft_ghg_emissions = Column(Float)
    characterization_factors = Column(Enum(CharacterizationFactors), nullable=False)
    cross_sectoral_standards_used = Column(String, nullable=False)
    biogenic_accounting_methodology = Column(Enum(BiogenicAccountingMethodology))
    boundary_processes_description = Column(String, nullable=False)
    reference_period_start = Column(DateTime, nullable=False)
    reference_period_end = Column(DateTime, nullable=False)
    geography_country_subdivision = Column(String)
    geography_country = Column(String(2))
    geography_region_or_subregion = Column(Enum(RegionOrSubregion))
    exempted_emissions_percent = Column(Float, CheckConstraint('exempted_emissions_percent BETWEEN 0 and 5'))
    exempted_emissions_description = Column(String, nullable=False)
    packaging_emissions_included = Column(Boolean, nullable=False)
    packaging_ghg_emissions = Column(Float)
    allocation_rules_description = Column(String)
    uncertainty_assessment_description = Column(String)
    primary_data_share = Column(Float)
    dqi = Column(JSONB)
    assurance = Column(JSONB)
    product_footprint_pk = Column(Integer, ForeignKey('productfootprint.pk'), comment="The carbon footprint of the given product.")
    product_footprint = relationship(
        "ProductFootprint", back_populates="carbon_footprint")
    product_or_sector_specific_rules = relationship(
        "ProductOrSectorSpecificRuleModel", back_populates="carbon_footprint"
    )
    secondary_emission_factor_sources = relationship(
        "EmissionFactorDatasetModel", back_populates="carbon_footprint"
    )
