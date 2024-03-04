from fastapi_pagination import paginate
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from apis.version1.route_login import get_current_user_from_token
from core.exceptions import NoSuchFootprintException
from core.pagination import JSONAPIPage
from db.models.user import User
from db.repository.product_footprints import create_new_product_footprint
from db.repository.product_footprints import list_product_footprints
from db.repository.product_footprints import retrieve_product_footprint
from db.session import get_db
from schemas.product_footprint import ProductFootprint as ProductFootprintSchema
from schemas.carbon_footprint import CarbonFootprint as CarbonFootprintSchema, EmissionFactorDS, ProductOrSectorSpecificRule


router = APIRouter()


"""
TODO: Implement full CRUD functionality for this module.
"""

@router.post("/create-product-footprint/", status_code=200)
def create_product_footprint(
    product_footprint: ProductFootprintSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    product_footprint = create_new_product_footprint(product_footprint=product_footprint, db=db)
    if product_footprint:
        return "Success"


@router.get("/{id}", response_model=dict[str, ProductFootprintSchema], status_code=200)
def read_product_footprint(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    product_footprint = retrieve_product_footprint(id=id, db=db)

    secondary_emission_factor_sources: list[EmissionFactorDS] = []
    for dataset in product_footprint.carbon_footprint.secondary_emission_factor_sources:
        dataset_schema = EmissionFactorDS(
            name=dataset.name,
            version=dataset.version
        )
        secondary_emission_factor_sources.append(dataset_schema)


    product_or_sector_specific_rules: list[ProductOrSectorSpecificRule] = []
    for rule in product_footprint.carbon_footprint.product_or_sector_specific_rules:
        rule_schema = ProductOrSectorSpecificRule(
            operator=rule.operator,
            ruleNames=rule.rule_names,
            otherOperatorName=rule.other_operator_name
        )
        product_or_sector_specific_rules.append(rule_schema)

    product_footprint_schema = ProductFootprintSchema(
        id=product_footprint.id,
        specVersion=product_footprint.specVersion,
        precedingPfIds=product_footprint.precedingPfIds,
        version=product_footprint.version,
        created=product_footprint.created,
        updated=product_footprint.updated,
        status=product_footprint.status,
        statusComment=product_footprint.statusComment,
        validityPeriodStart=product_footprint.validityPeriodStart,
        validityPeriodEnd=product_footprint.validityPeriodEnd,
        companyName=product_footprint.companyName,
        companyIds=product_footprint.companyIds,
        productDescription=product_footprint.productDescription,
        productIds=product_footprint.productIds,
        productCategoryCpc=product_footprint.productCategoryCpc,
        productNameCompany=product_footprint.productNameCompany,
        comment=product_footprint.comment,
        pcf=CarbonFootprintSchema(
            declaredUnit=product_footprint.carbon_footprint.declared_unit,
            unitaryProductAmount=product_footprint.carbon_footprint.unitary_product_amount,
            pCfExcludingBiogenic=product_footprint.carbon_footprint.pcf_excluding_biogenic,
            pcfIncludingBiogenic=product_footprint.carbon_footprint.pcf_including_biogenic,
            fossilGhgEmissions=product_footprint.carbon_footprint.fossil_ghg_emissions,
            fossilCarbonContent=product_footprint.carbon_footprint.fossil_carbon_content,
            biogenicCarbonContent=product_footprint.carbon_footprint.biogenic_carbon_content,
            dlucGhgEmissions=product_footprint.carbon_footprint.dluc_ghg_emissions,
            landManagementGhgEmissions=product_footprint.carbon_footprint.land_management_ghg_emissions,
            otherBiogenicGhgEmissions=product_footprint.carbon_footprint.other_biogenic_ghg_emissions,
            ilucGhgEmissions=product_footprint.carbon_footprint.iluc_ghg_emissions,
            biogenicCarbonWithdrawal=product_footprint.carbon_footprint.biogenic_carbon_withdrawal,
            aircraftGhgEmissions=product_footprint.carbon_footprint.aircraft_ghg_emissions,
            characterizationFactors=product_footprint.carbon_footprint.characterization_factors,
            crossSectoralStandardsUsed=product_footprint.carbon_footprint.cross_sectoral_standards_used,
            productOrSectorSpecificRules=product_or_sector_specific_rules,
            biogenicAccountingMethodology=product_footprint.carbon_footprint.biogenic_accounting_methodology,
            boundaryProcessesDescription=product_footprint.carbon_footprint.boundary_processes_description,
            referencePeriodStart=product_footprint.carbon_footprint.reference_period_start,
            referencePeriodEnd=product_footprint.carbon_footprint.reference_period_end,
            # missing additional fields for the other two geo fields, they are not in the database i dont think
            geographyRegionOrSubregion=product_footprint.carbon_footprint.geography_region_or_subregion,
            secondaryEmissionFactorSources=secondary_emission_factor_sources,
            exemptedEmissionsPercent=product_footprint.carbon_footprint.exempted_emissions_percent,
            exemptedEmissionsDescription=product_footprint.carbon_footprint.exempted_emissions_description,
            packagingEmissionsIncluded=product_footprint.carbon_footprint.packaging_emissions_included,
            packagingGhgEmissions=product_footprint.carbon_footprint.packaging_ghg_emissions,
            allocationRulesDescription=product_footprint.carbon_footprint.allocation_rules_description,
            uncertaintyAssessmentDescription=product_footprint.carbon_footprint.uncertainty_assessment_description,
            primaryDataShare=product_footprint.carbon_footprint.primary_data_share,
            dqi=product_footprint.carbon_footprint.dqi,
            assurance=product_footprint.carbon_footprint.assurance
        ),
        extensions=product_footprint.extensions
    )
    if not product_footprint:
        raise NoSuchFootprintException
    return {'data': product_footprint_schema}


@router.get("", response_model=JSONAPIPage[ProductFootprintSchema], status_code=200)
def list_footprints(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    """
    TODO: This route is currently not tested due to the pagination module being too difficult
        to programmatically interact with, during alpha, it will be tuned up and formed into
        something far more workable, and with that will come tests, currently it is not easy
        to understand, the code was added in so that the PoC could move forward and an ALpha
        release needs to happen sooner rather than later.
    """
    product_footprints = list_product_footprints(db=db)
    if not product_footprints:
        raise NoSuchFootprintException
    return paginate(product_footprints)
