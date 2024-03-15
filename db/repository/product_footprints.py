import pprint

from sqlalchemy.orm import Session

from db.models.product_footprint import ProductFootprint as ProductFootprintModel
from db.models.carbon_footprint import CarbonFootprintModel, ProductOrSectorSpecificRuleModel, EmissionFactorDatasetModel
from schemas.product_footprint import ProductFootprint as ProductFootprintSchema


pp = pprint.PrettyPrinter(depth=4)


def create_new_product_footprint(product_footprint: ProductFootprintSchema, db: Session):
    # TODO: Log this action

    product_or_sector_specific_rules: list[ProductOrSectorSpecificRuleModel] = []
    for each in product_footprint.pcf.productOrSectorSpecificRules:
        product_or_sector_specific_rules.append(
            ProductOrSectorSpecificRuleModel(
                operator=each.operator,
                rule_names=each.ruleNames,
                other_operator_name=each.otherOperatorName
            )
        )

    secondary_emission_factor_sources: list[EmissionFactorDatasetModel] = []
    for each in product_footprint.pcf.secondaryEmissionFactorSources:
        secondary_emission_factor_sources.append(
            EmissionFactorDatasetModel(
                name=each.name,
                version=each.version
            )
        )

    data_entry = ProductFootprintModel(
        id = product_footprint.id,
        precedingPfIds = product_footprint.precedingPfIds,
        specVersion = product_footprint.specVersion,
        version = product_footprint.version,
        created = product_footprint.created,
        updated = product_footprint.updated,
        status = product_footprint.status,
        statusComment = product_footprint.statusComment,
        validityPeriodStart = product_footprint.validityPeriodStart,
        validityPeriodEnd = product_footprint.validityPeriodEnd,
        companyName = product_footprint.companyName,
        companyIds = product_footprint.companyIds,
        productDescription = product_footprint.productDescription,
        productIds = product_footprint.productIds,
        productCategoryCpc = product_footprint.productCategoryCpc,
        productNameCompany = product_footprint.productNameCompany,
        comment = product_footprint.comment,
        carbon_footprint = CarbonFootprintModel(
            declared_unit=product_footprint.pcf.declaredUnit,
            unitary_product_amount=product_footprint.pcf.unitaryProductAmount,
            pcf_excluding_biogenic=product_footprint.pcf.pCfExcludingBiogenic,
            pcf_including_biogenic=product_footprint.pcf.pCfIncludingBiogenic,
            fossil_ghg_emissions=product_footprint.pcf.fossilGhgEmissions,
            fossil_carbon_content=product_footprint.pcf.fossilCarbonContent,
            biogenic_carbon_content=product_footprint.pcf.biogenicCarbonContent,
            dluc_ghg_emissions=product_footprint.pcf.dLucGhgEmissions,
            land_management_ghg_emissions=product_footprint.pcf.landManagementGhgEmissions,
            other_biogenic_ghg_emissions=product_footprint.pcf.otherBiogenicGhgEmissions,
            iluc_ghg_emissions=product_footprint.pcf.iLucGhgEmissions,
            biogenic_carbon_withdrawal=product_footprint.pcf.biogenicCarbonWithdrawal,
            aircraft_ghg_emissions=product_footprint.pcf.aircraftGhgEmissions,
            characterization_factors=product_footprint.pcf.characterizationFactors,
            cross_sectoral_standards_used=product_footprint.pcf.crossSectoralStandardsUsed,
            product_or_sector_specific_rules=product_or_sector_specific_rules,
            biogenic_accounting_methodology=product_footprint.pcf.biogenicAccountingMethodology,
            boundary_processes_description=product_footprint.pcf.boundaryProcessesDescription,
            reference_period_start=product_footprint.pcf.referencePeriodStart,
            reference_period_end=product_footprint.pcf.referencePeriodEnd,
            geography_region_or_subregion=product_footprint.pcf.geographyRegionOrSubregion,
            secondary_emission_factor_sources=secondary_emission_factor_sources,
            exempted_emissions_percent=product_footprint.pcf.exemptedEmissionsPercent,
            exempted_emissions_description=product_footprint.pcf.exemptedEmissionsDescription,
            packaging_emissions_included=product_footprint.pcf.packagingEmissionsIncluded,
            packaging_ghg_emissions=product_footprint.pcf.packagingGhgEmissions,
            allocation_rules_description=product_footprint.pcf.allocationRulesDescription,
            uncertainty_assessment_description=product_footprint.pcf.uncertaintyAssessmentDescription,
            primary_data_share=product_footprint.pcf.primaryDataShare,
            dqi=product_footprint.pcf.dqi,
            assurance=product_footprint.pcf.assurance
        ),
        extensions = product_footprint.extensions
    )
    # product_footprint_dict = product_footprint.model_dump()
    # # TODO: This is extremely ugly, we should be using some of the internal functionality
    # #      of pydantic here instead of mutating and casting the UUID id field.
    # product_footprint_dict['id'] = str(product_footprint_dict['id'])
    # product_footprint_dict['carbon_footprint'] = product_footprint_dict['pcf']
    # product_footprint_object = ProductFootprint(**product_footprint_dict)

    db.add(data_entry)
    db.commit()
    db.refresh(data_entry)
    return data_entry


def retrieve_product_footprint(id: str, db: Session):
    # TODO: I suspect another Pydantic field here to validate that a UUID formatted
    #   string is being passed here would be a winner, improve input validation
    item = db.query(ProductFootprintModel).filter(ProductFootprintModel.id == id).first()
    return item


def list_product_footprints(db: Session) -> list[ProductFootprintModel] | None:
    product_footprints = db.query(ProductFootprintModel).all()
    if len(product_footprints) == 0:
        return None
    return product_footprints


def count_product_footprints(db: Session):
    count = db.query(ProductFootprintModel).count()
    return count


def update_product_footprint_by_id(id: int, product_footprint: ProductFootprintSchema, db: Session, owner_id):
    existing_product_footprint = db.query(ProductFootprintModel).filter(ProductFootprintModel.id == id)
    if not existing_product_footprint.first():
        return 0
    product_footprint.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_product_footprint.update(product_footprint.__dict__)
    db.commit()
    return 1


def delete_product_footprint_by_id(id: int, db: Session, owner_id):
    existing_product_footprint = db.query(ProductFootprintModel).filter(ProductFootprintModel.id == id)
    if not existing_product_footprint.first():
        return 0
    existing_product_footprint.delete(synchronize_session=False)
    db.commit()
    return 1
