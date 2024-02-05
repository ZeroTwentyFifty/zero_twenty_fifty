import pytest


@pytest.fixture()
def valid_json_product_footprint():
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "specVersion": "string",
        "precedingPfids": [
            "3fa85f64-5717-4562-b3fc-2c963f66af10"
        ],
        "version": 1,
        "created": "2023-06-18T22:38:02.331Z",
        "updated": "2023-06-18T22:38:02.331Z",
        "status": "Active",
        "statusComment": "string",
        "validityPeriodStart": "2023-06-18T22:38:02.331Z",
        "validityPeriodEnd": "2023-06-18T22:38:02.331Z",
        "companyName": "Clean Product Company",
        "companyIds": [
                "urn:epc:id:sgln:0614141.00002.0"
        ],
        "productDescription": "string",
        "productIds": [
                "urn:epc:id:gtin:0614141.011111.0"
        ],
        "productCategoryCpc": "22222",
        "productNameCompany": "string",
        "comment": "string",
        "pcf": {
            "declaredUnit": "liter",
            "unitaryProductAmount": 0,
            "pCfExcludingBiogenic": 0,
            "pCfIncludingBiogenic": 0,
            "fossilGhgEmissions": 0,
            "fossilCarbonContent": 0,
            "biogenicCarbonContent": 0,
            "dlucGhgEmissions": 0,
            "landManagementGhgEmissions": 0,
            "otherBiogenicGhgEmissions": 0,
            "ilucGhgEmissions": 0,
            "biogenicCarbonWithdrawal": 0,
            "aircraftGhgEmissions": 0,
            "characterizationFactors": "string",
            "crossSectoralStandardsUsed": [
                    "GHG Protocol Product standard"
            ],
            "productOrSectorSpecificRules": [
                "Other", "string", "string"
            ],
            "biogenicAccountingMethodology": "PEF",
            "boundaryProcessesDescription": "string",
            "referencePeriodStart": "2023-06-18T22:38:02.332Z",
            "referencePeriodEnd": "2023-06-18T22:38:02.332Z",
            "geographyCountrySubdivision": "string",
            "geographyCountry": {
                "code": "AU"
            },
            "geographyRegionOrSubregion": "Africa",
            "secondaryEmissionFactorSources": {
                "datasets": [
                    {
                        "name": "string",
                        "version": "string"
                    }
                ]
            },
            "exemptedEmissionsPercent": 0,
            "exemptedEmissionsDescription": "string",
            "packagingEmissionsIncluded": True,
            "packagingGhgEmissions": 0,
            "allocationRulesDescription": "string",
            "uncertaintyAssessmentDescription": "string",
            "primaryDataShare": 0,
            "assurance": {
                "assurance": True,
                "coverage": "corporate level",
                "level": "limited",
                "boundary": "Gate-to-Gate",
                "providerName": "string",
                "completedAt": "2023-06-18T22:38",
                "standardName": "string",
                "comments": "string"
            }
        }
    }


@pytest.fixture
def test_credentials():
    return ("testuser@example.com", "testuser")


@pytest.fixture
def access_token(client, test_user):
    """
    TODO: Clean this up and instead of returning an access_token, just return the
        auth header so it can be inserted directly into the client requests, do
        this from the conftest file
    """
    response = client.post(
        "/auth/token",
        data={
            "grant_type": "",
            "scope": "",
            "client_id": "testuser@example.com",
            "client_secret": "testuser"
        },
    )

    return response.json()["access_token"]


def test_create_product_footprint(client, access_token, valid_json_product_footprint):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post(
        url="/footprints/create-product-footprint/",
        json=valid_json_product_footprint,
        headers=headers
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json() == "Success"


def test_read_product_footprint(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/footprints/3fa85f64-5717-4562-b3fc-2c963f66afa6/", headers=headers)

    assert response.status_code == 200
    assert response.json()["data"]["companyName"] == "Clean Product Company"


"""
TODO: re-enable this test when the pagination module is improved and cleaned up, the
    code for pagination throws runtime errors when tested programatically, as it was
    jacked from somewhere else in order to get it running, it needs to be looked over
    in a more structured way.

def test_read_product_footprints(client, access_token, valid_json_product_footprint):
    headers = {"Authorization": f"Bearer {access_token}"}

    client.post(url="/footprints/create-product-footprint/", json=json.dumps(valid_json_product_footprint))
    client.post(url="/footprints/create-product-footprint/", json=json.dumps(valid_json_product_footprint))

    response = client.get("/footprints/?offset=1&limit=10", headers=headers)
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]
"""
