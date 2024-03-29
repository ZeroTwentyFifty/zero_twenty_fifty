from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import (
    AwareDatetime, BaseModel, ConfigDict, Field, PositiveFloat, confloat, constr,
    field_serializer, model_validator
)

from schemas.base_types import NonEmptyString


class CharacterizationFactors(str, Enum):
    """
    The IPCC version of the GWP characterization factors used in the calculation of the PCF (see Pathfinder Framework Section 3.2.2).
    The value MUST be one of the following:

    - AR6: for the Sixth Assessment Report of the Intergovernmental Panel on Climate Change (IPCC)
    - AR5: for the Fifth Assessment Report of the IPCC.

    The set of characterization factor identifiers will likely change in future revisions.
    It is recommended to account for this when implementing the validation of this property.

    For more information, please refer to the official documentation:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#element-attrdef-carbonfootprint-characterizationfactors
    """
    AR5 = 'AR5'
    AR6 = 'AR6'


class BiogenicAccountingMethodology(str, Enum):
    """
    The standard followed to account for biogenic emissions and removals.
    If defined, the value MUST be one of the following:

    - PEF: For the EU Product Environmental Footprint Guide
    - ISO: For the ISO 14067 standard
    - GHGP: For the Greenhouse Gas Protocol (GHGP) Land sector and Removals Guidance
    - Quantis: For the Quantis Accounting for Natural Climate Solutions Guidance

    The enumeration of standards above will be evolved in future revisions.
    Account for this when implementing the validation of this property.

    For more information, please refer to the official documentation:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#element-attrdef-carbonfootprint-biogenicaccountingmethodology
    """
    PEF = 'PEF'
    ISO = 'ISO'
    GHGP = 'GHGP'
    QUANTIS = 'Quantis'


class DeclaredUnit(str, Enum):
    """
    DeclaredUnit is the enumeration of accepted declared units with values.

    The values are based on the International System of Units (SI) as defined by the International Committee for Weights and Measures (ICWM).

    - LITER: for special SI Unit litre
    - KILOGRAM: for SI Base Unit kilogram
    - CUBIC_METER: for cubic meter, the Derived Unit from SI Base Unit metre
    - KILOWATT_HOUR: for kilowatt hour, the Derived Unit from special SI Unit watt
    - MEGAJOULE: for megajoule, the Derived Unit from special SI Unit joule
    - TON_KILOMETER: for ton kilometer, the Derived Unit from SI Base Units kilogram and metre
    - SQUARE_METER: for square meter, the Derived Unit from SI Base Unit metre

    The value of each DeclaredUnit MUST be encoded as a JSON String.

    For more information, please refer to the official documentation:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#dt-declaredunit
    And the SI Unit reference:
        https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf/2d2b50bf-f2b4-9661-f402-5f9d66e4b507
    """
    LITER = 'liter'
    KILOGRAM = 'kilogram'
    CUBIC_METER = 'cubic meter'
    KILOWATT_HOUR = 'kilowatt hour'
    MEGAJOULE = 'megajoule'
    TON_KILOMETER = 'ton kilometer'
    SQUARE_METER = 'square meter'


class RegionOrSubregion(str, Enum):
    """The RegionOrSubregion data type represents a geographic region or subregion.

    It MUST be encoded as a String with value equal to one of the following values:

    - Africa: for the UN geographic region Africa
    - Americas: for the UN geographic region Americas
    - Asia: for the UN geographic region Asia
    - Europe: for the UN geographic region Europe
    - Oceania: for the UN geographic region Oceania
    - Australia and New Zealand: for the UN geographic subregion Australia and New Zealand
    - Central Asia: for the UN geographic subregion Central Asia
    - Eastern Asia: for the UN geographic subregion Eastern Asia
    - Eastern Europe: for the UN geographic subregion Eastern Europe
    - Latin America and the Caribbean: for the UN geographic subregion Latin America and the Caribbean
    - Melanesia: for the UN geographic subregion Melanesia
    - Micronesia: for the UN geographic subregion Micronesia
    - Northern Africa: for the UN geographic subregion Northern Africa
    - Northern America: for the UN geographic subregion Northern America
    - Northern Europe: for the UN geographic subregion Northern Europe
    - Polynesia: for the UN geographic subregion Polynesia
    - South-eastern Asia: for the UN geographic subregion South-eastern Asia
    - Southern Asia: for the UN geographic subregion Southern Asia
    - Southern Europe: for the UN geographic subregion Southern Europe
    - Sub-Saharan Africa: for the UN geographic subregion Sub-Saharan Africa
    - Western Asia: for the UN geographic subregion Western Asia
    - Western Europe: for the UN geographic subregion Western Europe

    For more information, please refer to the official documentation:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#dt-regionorsubregion
    """
    AFRICA = 'Africa'
    AMERICAS = 'Americas'
    ASIA = 'Asia'
    EUROPE = 'Europe'
    OCEANIA = 'Oceania'
    AUSTRALIA_AND_NEW_ZEALAND = 'Australia and New Zealand'
    CENTRAL_ASIA = 'Central Asia'
    EASTERN_ASIA = 'Eastern Asia'
    EASTERN_EUROPE = 'Eastern Europe'
    LATIN_AMERICA_AND_THE_CARIBBEAN = 'Latin America and the Caribbean'
    MELANESIA = 'Melanesia'
    MICRONESIA = 'Micronesia'
    NORTHERN_AFRICA = 'Northern Africa'
    NORTHERN_AMERICA = 'Northern America'
    NORTHERN_EUROPE = 'Northern Europe'
    POLYNESIA = 'Polynesia'
    SOUTH_EASTERN_ASIA = 'South-eastern Asia'
    SOUTHERN_ASIA = 'Southern Asia'
    SOUTHERN_EUROPE = 'Southern Europe'
    SUB_SAHARAN_AFRICA = 'Sub-Saharan Africa'
    WESTERN_ASIA = 'Western Asia'
    WESTERN_EUROPE = 'Western Europe'


class CrossSectoralStandard(str, Enum):
    """
    CrossSectoralStandard is the enumeration of accounting standards used for product carbon footprint calculation. Valid values are

    - GHG Protocol Product standard: for the GHG Protocol Product standard
    - ISO Standard 14067: for ISO Standard 14067
    - ISO Standard 14044: for ISO Standard 14044

    4.9.1. JSON Representation
    Each CrossSectoralStandard MUST be encoded as a JSON string.

    The value of each DeclaredUnit MUST be encoded as a JSON String.

    For more information, please refer to the official documentation:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#dt-crosssectoralstandard
    """
    GHG_PROTOCOL = 'GHG Protocol Product standard'
    ISO_14067 = 'ISO Standard 14067'
    ISO_14044 = 'ISO Standard 14044'


class ProductOrSectorSpecificRuleOperator(str, Enum):
    """
    A ProductOrSectorSpecificRuleOperator is the enumeration of Product Category Rule (PCR) operators. Valid values are:

    - PEF: for EU / PEF Methodology PCRs
    - EPD International: for PCRs authored or published by EPD International
    - Other: for a PCR not published by the operators mentioned above

    4.13.1. JSON Representation
    Each value is encoded as a JSON String.

    For more information, please refer to the official documentation:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#dt-productorsectorspecificruleoperator
    """
    PEF = 'PEF'
    EPD_INTERNATIONAL = 'EPD International'
    OTHER = 'Other'


class ProductOrSectorSpecificRule(BaseModel):
    """A ProductOrSectorSpecificRule refers to a set of product or sector specific rules published by a specific operator and applied during product carbon footprint calculation.

    Attributes:
        operator (ProductOrSectorSpecificRuleOperator): A ProductOrSectorSpecificRule MUST include the property operator with the value conforming to data type ProductOrSectorSpecificRuleOperator.
        ruleNames (NonEmptyStringVector): A ProductOrSectorSpecificRule MUST include the property ruleNames with value the non-empty set of rules applied from the specified operator.
        otherOperatorName (NonEmptyString): If the value of property operator is Other, a ProductOrSectorSpecificRule MUST include the property otherOperatorName with value the name of the operator. In this case, the operator declared MUST NOT be included in the definition of ProductOrSectorSpecificRuleOperator. If the value of property operator is NOT Other, the property otherOperatorName of a ProductOrSectorSpecificRule MUST be undefined.

    JSON Representation
        Each ProductOrSectorSpecificRule MUST be encoded as a JSON object.

    For more information, please refer to the official documentation:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#dt-productorsectorspecificrule
    """
    operator: ProductOrSectorSpecificRuleOperator = Field(..., description="A ProductOrSectorSpecificRule MUST include the property operator with the value conforming to data type ProductOrSectorSpecificRuleOperator.")
    ruleNames: List[NonEmptyString] = Field(..., min_length=1, description="A ProductOrSectorSpecificRule MUST include the property ruleNames with value the non-empty set of rules applied from the specified operator.")  # Mandatory, non-empty

    # Optional field with conditional dependency
    otherOperatorName: Optional[NonEmptyString] = Field(
        None,
        description='If the value of property operator is Other, a ProductOrSectorSpecificRule MUST include the property otherOperatorName with value the name of the operator. In this case, the operator declared MUST NOT be included in the definition of ProductOrSectorSpecificRuleOperator. If the value of property operator is NOT Other, the property otherOperatorName of a ProductOrSectorSpecificRule MUST be undefined.',
    )

    # Using a validator for precise dependency logic
    @model_validator(mode='after')
    def validate_other_operator_name(self):
        if self.operator == ProductOrSectorSpecificRuleOperator.OTHER and not self.otherOperatorName:
            raise ValueError("'otherOperatorName' is required when 'operator' is 'Other'")
        if self.operator != ProductOrSectorSpecificRuleOperator.OTHER and self.otherOperatorName:
            raise ValueError("'otherOperatorName' must be absent when 'operator' is not 'Other'")
        return self


class EmissionFactorDS(BaseModel):
    """Represents an EmissionFactorDS, referencing emission factor databases.

    For further details, please refer to the Pathfinder Framework Section 4.1.3.2.

    Attributes:
        name (NonEmptyString): The name of the emission factor database. Must be non-empty.
        version (NonEmptyString): The version of the emission factor database. Must be non-empty.

    Each EmissionFactorDS MUST be encoded as a JSON object.
    Example:
        {
          "name": "ecoinvent",
          "version": "3.9.1"
        }

    For more information, please refer to the official documentation:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#dt-emissionfactords
    """
    name: NonEmptyString = Field(..., description="The non-empty name of the emission factor database.")
    version: NonEmptyString = Field(..., description="The non-empty version of the emission factor database.")


class CarbonFootprint(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True
    )
    declaredUnit: DeclaredUnit = Field(
        ...,
        description="DeclaredUnit is the enumeration of accepted declared units with values"
    )
    unitaryProductAmount: PositiveFloat = Field(
        ...,
        description='Amount of declared units in the product (must be greater than 0).',
    )
    pCfExcludingBiogenic: confloat(ge=0.0) = Field(
        ...,
        description='Product carbon footprint excluding biogenic CO2 emissions (kgCO2e/declaredUnit).',
    )
    pCfIncludingBiogenic: Optional[float] = Field(
        None,
        description='Product carbon footprint including all biogenic emissions (kgCO2e/declaredUnit).',
    )
    fossilGhgEmissions: confloat(ge=0.0) = Field(
        ..., description='Emissions from fossil sources (kgCO2e/declaredUnit).'
    )
    fossilCarbonContent: confloat(ge=0.0) = Field(
        ..., description='Fossil carbon content of the product (kgC/declaredUnit).'
    )
    biogenicCarbonContent: confloat(ge=0.0) = Field(
        ..., description='Biogenic carbon content of the product (kgC/declaredUnit).'
    )
    dLucGhgEmissions: Optional[confloat(ge=0.0)] = Field(
        None,
        description='Emissions from recent direct land use change (kgCO2e/declaredUnit).',
    )
    landManagementGhgEmissions: Optional[float] = Field(
        None,
        description='Emissions/removals from land management (kgCO2e/declaredUnit).',
    )
    otherBiogenicGhgEmissions: Optional[confloat(ge=0.0)] = Field(
        None,
        description='Other biogenic GHG emissions not in dLUC or landManagement (kgCO2e/declaredUnit).',
    )
    iLucGhgEmissions: Optional[confloat(ge=0.0)] = Field(
        None,
        description='Emissions from recent indirect land use change (kgCO2e/declaredUnit).',
    )
    biogenicCarbonWithdrawal: Optional[confloat(le=0.0)] = Field(
        None,
        description='Biogenic carbon contained in the product converted to kgCO2e (must be less than or equal to zero).',
    )
    aircraftGhgEmissions: Optional[confloat(ge=0.0)] = Field(
        None,
        description='GHG emissions from aircraft usage for product transport (kgCO2e/declaredUnit).',
    )
    characterizationFactors: CharacterizationFactors = Field(
        ...,
        description='The IPCC Global Warming Potential characterization factors used.',
    )
    crossSectoralStandardsUsed: List[CrossSectoralStandard] = Field(
        ...,
        description='Cross-sectoral standards applied for calculating GHG emissions.',
    )
    productOrSectorSpecificRules: Optional[List[ProductOrSectorSpecificRule]] = Field(
        None,
        description='Product- or sector-specific rules for calculating GHG emissions.',
    )
    biogenicAccountingMethodology: Optional[BiogenicAccountingMethodology] = Field(
        None,
        description='The standard followed to account for biogenic emissions and removals.',
    )
    boundaryProcessesDescription: str = Field(
        ..., description='Description of processes included in each lifecycle stage.'
    )
    referencePeriodStart: AwareDatetime = Field(
        ..., description='Start of the time boundary for the PCF (ISO 8601)'
    )
    referencePeriodEnd: AwareDatetime = Field(
        ..., description='End of the time boundary for the PCF (ISO 8601)'
    )
    geographyCountrySubdivision: Optional[str] = Field(
        None, description='ISO 3166-2 Subdivision Code if applicable.'
    )
    geographyCountry: Optional[constr(pattern=r'^[A-Z]{2}$')] = Field(
        None, description='ISO 3166 Country Code if applicable.'
    )
    geographyRegionOrSubregion: Optional[RegionOrSubregion] = None
    secondaryEmissionFactorSources: Optional[List[EmissionFactorDS]] = Field(
        None, description='List of emission factor sources for secondary data, if used.'
    )
    exemptedEmissionsPercent: confloat(ge=0.0, le=5.0) = Field(
        ..., description='Percentage of emissions exempted from PCF (0 to 5).'
    )
    exemptedEmissionsDescription: str = Field(
        ..., description='Reasoning for excluding emissions.'
    )
    packagingEmissionsIncluded: bool = Field(
        ..., description='Indicates if packaging emissions are in the PCF.'
    )
    packagingGhgEmissions: Optional[confloat(ge=0.0)] = Field(
        None, description='Emissions from product packaging (kgCO2e/declaredUnit).'
    )
    allocationRulesDescription: Optional[str] = Field(
        None, description='Description of any allocation rules applied.'
    )
    uncertaintyAssessmentDescription: Optional[str] = Field(
        None, description='Description of the uncertainty assessment.'
    )
    primaryDataShare: Optional[confloat(ge=0.0, le=100.0)] = Field(
        None, description='The share of primary data in percent.'
    )
    dqi: Optional[Dict[str, Any]] = Field(
        None, description='Data Quality Indicators, if applicable.'
    )
    assurance: Optional[Dict[str, Any]] = Field(
        None, description='Assurance information, if applicable.'
    )

    @field_serializer('referencePeriodStart')
    def serialize_reference_period_start(self, referencePeriodStart: AwareDatetime, _info):
        return referencePeriodStart.isoformat()

    @field_serializer('referencePeriodEnd')
    def serialize_reference_period_end(self, referencePeriodEnd: AwareDatetime, _info):
        return referencePeriodEnd.isoformat()

