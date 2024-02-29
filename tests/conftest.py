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
from db.session import get_db
from db.repository.users import create_new_user
from schemas.user import UserCreate




def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    add_pagination(_app)

    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def test_user(db_session: SessionTesting):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testuser",
    }
    user = create_new_user(user=UserCreate(**user_data), db=db_session)
    return user


"""
TODO: Consolidate and clean up the fixtures across the tests, if there are fixtures that
are duplicates across files, look into putting them in one place and having the system
set itself up easily. A good place to start would probably be just learning a bit more
about good quality fixture organisation in Pytest.
"""


@pytest.fixture(scope="module")
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
        "productOrSectorSpecificRules": ["CFS Guidance for XYZ Sector"],
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