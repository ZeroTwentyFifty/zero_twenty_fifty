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
# def test_read_product_footprints(client, access_token, valid_json_product_footprint):
#     headers = {"Authorization": f"Bearer {access_token}"}
#
#     valid_json_product_footprint["id"] = str(uuid.uuid4())
#
#     post_response = client.post(url="/footprints/create-product-footprint/", json=json.dumps(valid_json_product_footprint), headers=headers)
#     client.post(url="/footprints/create-product-footprint/", json=json.dumps(valid_json_product_footprint))
#     assert post_response.json() == "Success"
#     response = client.get("/footprints/?offset=1&limit=10", headers=headers)
#     assert response.status_code == 200
#     print(response.json()["data"])
#     assert response.json()["data"]
#     # assert response.json()[1]
