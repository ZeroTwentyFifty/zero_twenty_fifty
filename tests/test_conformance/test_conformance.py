import time
import random
from urllib.parse import urlsplit, urlunsplit
from datetime import datetime, timedelta

import freezegun
import pytest


@pytest.fixture
def test_credentials():
    return ("testuser@example.com", "testuser")


@pytest.mark.conformance
def test_001_authentication_against_default_endpoint_success(client, test_user, test_credentials):
    """Test Case 001: Authentication against default endpoint - Success"""
    username, password = test_credentials

    response = client.post(
        "/auth/token",
        data={
            "grant_type": "",
            "scope": "",
            "client_id": username,
            "client_secret": password
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.conformance
@pytest.mark.xfail(
    reason="Failure expected as we have implemented /auth/token according to spec",
    strict=True
)
def test_001_authentication_against_default_endpoint_failure(client):
    """Test Case 001: Authentication against default endpoint - Failure"""
    test_username = "invalid_username"
    test_password = "invalid_password"

    response = client.post(
        "/auth/token",
        data={
            "grant_type": "",
            "scope": "",
            "client_id": test_username,
            "client_secret": test_password
        },
    )

    assert response.status_code == 400
    assert "error" in response.json()


@pytest.mark.conformance
def test_002_authentication_with_invalid_credentials_against_default_endpoint(client):
    """Test Case 002: Authentication with invalid credentials against default endpoint"""
    test_username = "invalid_username"
    test_password = "invalid_password"

    response = client.post(
        "/auth/token",
        data={
            "grant_type": "",
            "scope": "",
            "client_id": test_username,
            "client_secret": test_password
        },
    )

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_client"


@pytest.mark.conformance
def test_003_get_all_footprints(client, auth_header):
    """Test Case 003: Get All Footprints"""
    response = client.get("/2/footprints/", headers=auth_header)

    assert response.status_code == 200
    assert "data" in response.json()


@pytest.mark.conformance
def test_004_get_limited_list_of_footprints(client, auth_header):
    """Test Case 004: Get Limited List of Footprints"""
    limit = 2
    response = client.get(f"/2/footprints/?limit={limit}", headers=auth_header)

    assert response.status_code == 200
    assert len(response.json()["data"]) <= limit

    # Check if Link header is present if total number of PCFs is greater than limit
    if len(response.json()["data"]) == limit:
        assert "Link" in response.headers


# This test doesn't work as intended
@pytest.mark.conformance
def test_005_pagination_link_implementation_of_action_listfootprints(client, auth_header):
    """Test Case 005: Pagination link implementation of Action ListFootprints"""

    # First, we need to get a pagination link from the Link header
    limit = 2
    response = client.get(f"/2/footprints/?limit={limit}", headers=auth_header)

    assert response.status_code == 200
    assert len(response.json()["data"]) <= limit

    if len(response.json()["data"]) == limit:
        assert "Link" in response.headers

        # Extract the pagination link from the Link header
        link_header = response.headers["Link"]
        links = [l.strip() for l in link_header.split(',')]
        pagination_link = random.choice(links)

        # Extract the URL from the pagination link
        url_parts = urlsplit(pagination_link.split(';')[0].strip('<>'))
        pagination_url = urlunsplit((url_parts.scheme, url_parts.netloc, url_parts.path, url_parts.query, ''))

        # Now, call the pagination link multiple times and check the responses
        start_time = time.time()
        responses = []
        for _ in range(3):  # Call the pagination link 3 times
            response = client.get(pagination_url, headers=auth_header)
            responses.append(response)

        # Check that all calls completed within 180 seconds
        assert time.time() - start_time <= 180

        # Check that all responses have the same status code and JSON body
        status_codes = [response.status_code for response in responses]
        json_bodies = [response.json() for response in responses]

        assert all(code == 200 or code == 202 for code in status_codes)
        assert all(body == json_bodies[0] for body in json_bodies)


@pytest.mark.conformance
def test_006_attempt_listfootprints_with_expired_token(client, auth_header):
    """Test Case 006: Attempt ListFootprints with Expired Token"""

    with freezegun.freeze_time(datetime.utcnow() + timedelta(days=1)):
        response = client.get("/2/footprints/", headers=auth_header)

        assert response.status_code == 401
        assert response.json() == {
            "message": "The specified access token has expired",
            "code": "TokenExpired"
        }


@pytest.mark.conformance
def test_007_attempt_listfootprints_with_invalid_token(client):
    """Test Case 007: Attempt ListFootprints with Invalid Token"""

    # Create an invalid token by modifying a valid token
    invalid_token = 'invalid-token'
    invalid_auth_header = {'Authorization': f'Bearer {invalid_token}'}

    response = client.get("/2/footprints/", headers=invalid_auth_header)

    assert response.status_code == 403
    assert response.json()["code"] == "AccessDenied"


@pytest.mark.conformance
def test_008_get_footprint(client, auth_header, valid_json_product_footprint):
    """Test Case 008: Get Footprint"""

    # Create a new footprint
    response = client.post(
        url="/2/footprints/create-product-footprint/",
        json=valid_json_product_footprint,
        headers=auth_header
    )

    # Get the pfId of the newly created footprint
    pf_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    response = client.get(
        url=f"/2/footprints/{pf_id}/",
        headers=auth_header
    )

    assert response.status_code == 200
    assert response.json()["data"]["id"] == pf_id


@pytest.mark.conformance
def test_009_attempt_getfootprint_with_expired_token(client, auth_header):
    """Test Case 009: Attempt GetFootprint with Expired Token"""

    # Create an expired token by moving the clock forward by one day
    with freezegun.freeze_time(datetime.utcnow() + timedelta(days=1)):
        response = client.get("/2/footprints/3fa85f64-5717-4562-b3fc-2c963f66afa6/", headers=auth_header)

        assert response.status_code == 401
        assert response.json()["code"] == "TokenExpired"


@pytest.mark.conformance
def test_010_attempt_getfootprint_with_invalid_token(client):
    """Test Case 010: Attempt GetFootprint with Invalid Token"""

    # Create an invalid token by modifying a valid token
    invalid_token = 'invalid-token'
    invalid_auth_header = {'Authorization': f'Bearer {invalid_token}'}

    response = client.get("/2/footprints/3fa85f64-5717-4562-b3fc-2c963f66afa6/", headers=invalid_auth_header)

    assert response.status_code == 403
    assert response.json()["code"] == "AccessDenied"


@pytest.mark.conformance
def test_011_attempt_getfootprint_with_non_existent_pf_id(client, auth_header):
    """Test Case 011: Attempt GetFootprint with Non-Existent PfId"""

    # Create a non-existent pfId
    non_existent_pf_id = 'non-existent-pf-id'

    response = client.get(f"/2/footprints/{non_existent_pf_id}/", headers=auth_header)

    assert response.status_code == 404
    assert response.json()["code"] == "NoSuchFootprint"
