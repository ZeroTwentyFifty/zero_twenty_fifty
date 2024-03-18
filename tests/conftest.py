import os
import sys
from datetime import datetime, timezone
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_pagination import add_pagination
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include backend dir in sys.path so that we can import from db,main.py

from apis.base import api_router
from db.base import Base
from db.models.product_footprint import ProductFootprint, ProductFootprintStatus
from db.models.carbon_footprint import CarbonFootprintModel, ProductOrSectorSpecificRuleModel, EmissionFactorDatasetModel
from schemas.carbon_footprint import (
    CharacterizationFactors, BiogenicAccountingMethodology, DeclaredUnit, RegionOrSubregion,
    ProductOrSectorSpecificRuleOperator
)
from db.session import get_db
from db.repository.users import create_new_user
from schemas.user import UserCreate




def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, future=True
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    add_pagination(_app)

    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_user(db_session: SessionTesting):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testuser",
    }
    user = create_new_user(user=UserCreate(**user_data), db=db_session)
    return user


@pytest.fixture
def auth_header(client, test_user):
    response = client.post(
        "/auth/token",
        data={
            "grant_type": "",
            "scope": "",
            "client_id": "testuser@example.com",
            "client_secret": "testuser"
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


"""
TODO: Consolidate and clean up the fixtures across the tests, if there are fixtures that
are duplicates across files, look into putting them in one place and having the system
set itself up easily. A good place to start would probably be just learning a bit more
about good quality fixture organisation in Pytest.
"""


@pytest.fixture
def valid_carbon_footprint_data():
    data = {
        "declaredUnit": "kilogram",
        "unitaryProductAmount": 100,
        "pCfExcludingBiogenic": 10,
        "pCfIncludingBiogenic": 12,
        "fossilGhgEmissions": 8,
        "fossilCarbonContent": 5,
        "biogenicCarbonContent": 4,
        "dLucGhgEmissions": 2,
        "landManagementGhgEmissions": 3,
        "otherBiogenicGhgEmissions": 1,
        "iLucGhgEmissions": 2,
        "biogenicCarbonWithdrawal": -1,
        "aircraftGhgEmissions": 0.5,
        "characterizationFactors": "AR6",
        "crossSectoralStandardsUsed": ["GHG Protocol Product standard"],
        "productOrSectorSpecificRules": [
            {
                "operator": "PEF",
                "ruleNames": ["EN15804+A2"]
            },
            {
                "operator": "Other",
                "ruleNames": ["CFS Guidance for XYZ Sector"],
                "otherOperatorName": "CFS"
            }
        ],
        "biogenicAccountingMethodology": "PEF",
        "boundaryProcessesDescription": "Description of boundary processes",
        "referencePeriodStart": datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat(),
        "referencePeriodEnd": datetime(2023, 12, 31, tzinfo=timezone.utc).isoformat(),
        "geographyCountrySubdivision": "AU",
        "geographyCountry": "AU",
        "geographyRegionOrSubregion": "Australia and New Zealand",
        "secondaryEmissionFactorSources": [
            {
                "name": "ecoinvent",
                "version": "3.9.1"
            }
        ],
        "exemptedEmissionsPercent": 2.5,
        "exemptedEmissionsDescription": "Description of exempted emissions",
        "packagingEmissionsIncluded": True,
        "packagingGhgEmissions": 0.5,
        "allocationRulesDescription": "Description of allocation rules",
        "uncertaintyAssessmentDescription": "Description of uncertainty assessment",
        "primaryDataShare": 50,
        "dqi": {"key1": "value1", "key2": "value2"},
        "assurance": {"key1": "value1", "key2": "value2"}
    }

    return data

@pytest.fixture
def valid_product_footprint_model():
    return ProductFootprint(
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
        extensions={}
    )


@pytest.fixture
def valid_carbon_footprint_model():
    return CarbonFootprintModel(
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
    )
