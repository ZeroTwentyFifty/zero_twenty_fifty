import uuid
from datetime import datetime, timezone, timedelta

import freezegun
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

@pytest.fixture(scope="function")
def seed_database(client, auth_header, valid_json_product_footprint, num_footprints=5):
    """Seeds the database with a specified number of product footprints.

    Args:
        client: The test client to make requests.
        auth_header: Authentication headers for the request.
        num_footprints: Number of footprints to add.
    """
    for i in range(num_footprints):
        updated_uuid_pf = valid_json_product_footprint.copy()
        updated_uuid_pf["id"] = str(uuid.uuid4())
        updated_uuid_pf["productCategoryCpc"] = str(22220 + i)
        response = client.post(
            url="/2/footprints/create-product-footprint/",
            json=updated_uuid_pf,
            headers=auth_header
        )
        assert response.status_code == 200
        assert response.json() == "Success"


def test_list_product_footprints_path_structure(client):
    response = client.get("/footprints/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_create_product_footprint(client, auth_header, valid_json_product_footprint):
    response = client.post(
        url="/2/footprints/create-product-footprint/",
        json=valid_json_product_footprint,
        headers=auth_header
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json() == "Success"


def test_create_product_footprint_with_expired_token(client, auth_header, valid_json_product_footprint):
    with freezegun.freeze_time(datetime.utcnow() + timedelta(days=1)):

        response = client.post(
            url="/2/footprints/create-product-footprint/",
            json=valid_json_product_footprint,
            headers=auth_header
        )

        assert response.status_code == 401
        assert response.json() == {
            "message": "The specified access token has expired",
            "code": "TokenExpired"
        }


def test_read_product_footprint(client, auth_header, valid_json_product_footprint):
    _ = client.post(
        url="/2/footprints/create-product-footprint/",
        json=valid_json_product_footprint,
        headers=auth_header
    )

    response = client.get(
        url="/2/footprints/3fa85f64-5717-4562-b3fc-2c963f66afa6/",
        headers=auth_header)

    assert response.status_code == 200
    assert response.json()["data"]["companyName"] == "Clean Product Company"


def test_read_product_footprint_with_expired_token(client, auth_header, valid_json_product_footprint):
    _ = client.post(
        url="/2/footprints/create-product-footprint/",
        json=valid_json_product_footprint,
        headers=auth_header
    )
    with freezegun.freeze_time(datetime.utcnow() + timedelta(days=1)):

        response = client.get(
            url="/2/footprints/3fa85f64-5717-4562-b3fc-2c963f66afa6/",
            headers=auth_header)

        assert response.status_code == 401
        assert response.json() == {
            "message": "The specified access token has expired",
            "code": "TokenExpired"
        }


def test_read_product_footprint_not_found(client, auth_header):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(
        url=f"/2/footprints/{non_existent_id}/",
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "The specified footprint does not exist"


def test_list_product_footprints_not_found(client, auth_header):
    response = client.get("/2/footprints/", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 0


def test_list_product_footprint_with_expired_token(client, auth_header, valid_json_product_footprint):
    with freezegun.freeze_time(datetime.utcnow() + timedelta(days=1)):

        response = client.get("/2/footprints/", headers=auth_header)

        assert response.status_code == 401
        assert response.json() == {
            "message": "The specified access token has expired",
            "code": "TokenExpired"
        }


def test_read_product_footprints(client, auth_header, seed_database):
    response = client.get("/2/footprints/", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5
    assert response.json()
    assert response.json()["data"][1]
    assert response.json()["data"][4]


def test_read_product_footprints_with_offset(client, auth_header, seed_database):
    response = client.get("/2/footprints/?offset=3", headers=auth_header)
    assert response.status_code == 200
    print(f"data = {response.json()['data']}")
    assert len(response.json()["data"]) == 2
    assert response.json()
    assert response.json()["data"][0]
    assert response.json()["data"][1]


def test_read_product_footprints_with_limit(client, auth_header, seed_database):
    response = client.get("/2/footprints/?limit=3", headers=auth_header)
    assert response.status_code == 200
    print(f"data = {response.json()['data']}")
    assert len(response.json()["data"]) == 3
    assert response.json()
    assert response.json()["data"][1]
    assert response.json()["data"][2]


@pytest.mark.xfail(reason="Filter feature not implemented", strict=True)
def test_list_product_footprints_with_filter_eq(client, auth_header, seed_database):
    filter_param = "$filter=productCategoryCpc eq '22222'"
    response = client.get(f"/2/footprints/?{filter_param}", headers=auth_header)
    assert response.status_code == 200
    footprints = response.json()["data"]
    assert len(footprints) == 1  # Assert that only 1 footprint is returned
    for footprint in footprints:
        assert int(footprint["productCategoryCpc"]) == 22222


@pytest.mark.xfail(reason="Filter feature not implemented", strict=True)
def test_list_product_footprints_with_filter_lt(client, auth_header, seed_database):
    filter_param = "$filter=productCategoryCpc lt '22222'"
    response = client.get(f"/2/footprints/?{filter_param}", headers=auth_header)
    assert response.status_code == 200
    footprints = response.json()["data"]
    assert len(footprints) == 2  # Assert that 2 footprints are returned
    for footprint in footprints:
        assert int(footprint["productCategoryCpc"]) < 22222


@pytest.mark.xfail(reason="Filter feature not implemented", strict=True)
def test_list_product_footprints_with_filter_le(client, auth_header, seed_database):
    filter_param = "$filter=productCategoryCpc le '22222'"
    response = client.get(f"/2/footprints/?{filter_param}", headers=auth_header)
    assert response.status_code == 200
    footprints = response.json()["data"]
    assert len(footprints) == 3  # Assert that 3 footprints are returned
    for footprint in footprints:
        assert int(footprint["productCategoryCpc"]) <= 22222


@pytest.mark.xfail(reason="Filter feature not implemented", strict=True)
def test_list_product_footprints_with_filter_gt(client, auth_header, seed_database):
    filter_param = "$filter=productCategoryCpc gt '22222'"
    response = client.get(f"/2/footprints/?{filter_param}", headers=auth_header)
    assert response.status_code == 200
    footprints = response.json()["data"]
    assert len(footprints) == 2  # Assert that 2 footprints are returned
    for footprint in footprints:
        assert int(footprint["productCategoryCpc"]) > 22222


@pytest.mark.xfail(reason="Filter feature not implemented", strict=True)
def test_list_product_footprints_with_filter_ge(client, auth_header, seed_database):
    filter_param = "$filter=productCategoryCpc ge '22222'"
    response = client.get(f"/2/footprints/?{filter_param}", headers=auth_header)
    assert response.status_code == 200
    footprints = response.json()["data"]
    assert len(footprints) == 3  # Assert that 3 footprints are returned
    for footprint in footprints:
        assert int(footprint["productCategoryCpc"]) >= 22222

# add a test for bad requests, when i hit "/footprints/?limit=50, it returned a NoneType
# error for the product_footprint call with has no attribute, need to catch that better
