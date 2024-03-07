import uuid
from datetime import datetime, timezone

import pytest


@pytest.fixture()
def valid_json_product_footprint(valid_carbon_footprint_data):
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
        "validityPeriodStart": datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat(),
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
        "pcf": valid_carbon_footprint_data
    }

@pytest.fixture()
def seed_database(client, auth_header, valid_json_product_footprint ,num_footprints=5):
    """Seeds the database with a specified number of product footprints.

    Args:
        client: The test client to make requests.
        auth_header: Authentication headers for the request.
        num_footprints: Number of footprints to add.
    """
    for _ in range(num_footprints):
        updated_uuid_pf = valid_json_product_footprint.copy()
        updated_uuid_pf["id"] = str(uuid.uuid4())
        response = client.post(
            url="/footprints/create-product-footprint/",
            json=updated_uuid_pf,
            headers=auth_header
        )
        assert response.status_code == 200
        assert response.json() == "Success"


def test_create_product_footprint(client, auth_header, valid_json_product_footprint):
    response = client.post(
        url="/footprints/create-product-footprint/",
        json=valid_json_product_footprint,
        headers=auth_header
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json() == "Success"


def test_read_product_footprint(client, auth_header):
    response = client.get(
        url="/footprints/3fa85f64-5717-4562-b3fc-2c963f66afa6/",
        headers=auth_header)

    assert response.status_code == 200
    assert response.json()["data"]["companyName"] == "Clean Product Company"


"""
This tests is currently succeeding but only because the create-product-footprint
calls are failing and so there's nothing in there, the API does actually work, but
this test does not, come back to this once the data model is in better shape.
"""
def test_read_product_footprints(client, auth_header, seed_database):

    response = client.get("/footprints/?offset=1&limit=10", headers=auth_header)
    assert response.status_code == 200
    print(f"data = {response.json()['data']}")
    assert len(response.json()["data"]) == 5
    assert response.json()
    assert response.json()["data"][1]
    assert response.json()["data"][4]
