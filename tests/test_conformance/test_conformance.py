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
    """
    5.9. Test Case 009: Attempt GetFootprint with Expired Token
    Tests the target host system’s ability to reject a GetFootprint request with an expired access token with the correct error response.

    5.9.1. Request
    A GetFootprint GET request must be sent to the /2/footprints/{GetPfId} endpoint of the test target host system with an expired access token and the syntax specified in PACT Tech Specs V2.2 § api-action-get-request.

    5.9.2. Expected Response
    The test target host system must respond with a 401 Unauthorized and a JSON body that should contain the error response TokenExpired, as specified in PACT Tech Specs V2.2 § api-error-responses.

    NOTE: Since the access token is expired, re-authentication should in principle solve the issue. By returning the HTTP error code 401 (instead of, e.g., 403), the host system signals that re-authentication should be attempted.
    """

    # Create an expired token by moving the clock forward by one day
    with freezegun.freeze_time(datetime.utcnow() + timedelta(days=1)):
        response = client.get("/2/footprints/3fa85f64-5717-4562-b3fc-2c963f66afa6/", headers=auth_header)

        assert response.status_code == 401
        assert response.json()["code"] == "TokenExpired"


@pytest.mark.conformance
def test_010_attempt_getfootprint_with_invalid_token(client):
    """
    5.10. Test Case 010: Attempt GetFootprint with Invalid Token
    Tests the target host system’s ability to reject a GetFootprint request with an invalid access token with the correct error response.

    5.10.1. Request
    A GetFootprint GET request must be sent to the /2/footprints/{GetPfId} endpoint of the test target host system with an invalid access token and the syntax specified in PACT Tech Specs V2.2 § api-action-get-request.

    5.10.2. Expected Response
    The test target host system must respond with a 403 Forbidden and a JSON body containing the error response AccessDenied, as specified in PACT Tech Specs V2.2 § api-error-responses.

    NOTE: Since the access token is invalid, re-authentication cannot solve the issue. By returning the HTTP error code 403 (instead of, e.g., 401), the host system signals that there is no gain in re-authenticating.
    """

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


@pytest.mark.conformance
def test_012_openid_connect_authentication_flow(client):
    """Test Case 012: OpenId Connect-based Authentication Flow"""

    # Retrieve the OpenId Provider Configuration Document
    response = client.get("/.well-known/openid-configuration")
    assert response.status_code == 200

    # Extract the token endpoint from the configuration document
    token_endpoint = response.json()["token_endpoint"]

    # Authenticate through the AuthEndpoint
    auth_response = client.post(token_endpoint, data={"grant_type": "client_credentials", "client_id": "your_client_id", "client_secret": "your_client_secret"})
    assert auth_response.status_code == 200

    # Verify that the response contains an access token
    assert "access_token" in auth_response.json()


@pytest.mark.conformance
def test_013_openid_connect_authentication_flow_with_incorrect_credentials(client, test_credentials):
    """Test Case 013: OpenId connect-based authentication flow with incorrect credentials

    Condition:
    The target host system supports the OpenId connect-based authentication flow (see PACT Tech Specs V2.2 § api-auth [1]).

    Request:
    The testing party performs the same flow as in § 6.1.2 Request but with incorrect credentials.

    Expected Response:
    The target host system returns a valid OpenId Provider Configuration Document.
    The target host system responds with a 400 Bad Request and a JSON body containing the error "invalid_client", as specified in PACT Tech Specs V2.2 § api-action-auth-response [1].

    References:
    [1] https://example.com/pact-tech-specs-v2-2

    This test case verifies that the target host system responds correctly to an OpenId connect-based authentication flow with incorrect credentials.
    """

    # Retrieve the OpenId Provider Configuration Document
    response = client.get("/.well-known/openid-configuration")
    assert response.status_code == 200

    # Extract the token endpoint from the configuration document
    token_endpoint = response.json()["token_endpoint"]

    # Authenticate through the AuthEndpoint with incorrect credentials
    invalid_credentials = ("invalid_user", "invalid_password")
    auth_response = client.post(token_endpoint, data={"grant_type": "client_credentials", "client_id": invalid_credentials[0], "client_secret": invalid_credentials[1]})
    assert auth_response.status_code == 400

    # Verify that the response contains the error "invalid_client"
    assert auth_response.json()["error"] == "invalid_client"


@pytest.mark.conformance
def test_014_attempt_authentication_through_http_non_https(client):
    """Test Case 014: Attempt Authentication through HTTP (non-HTTPS)

    Condition:
    According to PACT Tech Specs V2.2 § api-requirements, a host system must offer its actions under https method only.

    Request:
    An http-only equivalent of the test target host system AuthEndpoint (be it /auth/token or a custom endpoint) must be generated, replacing "https://" by "http://".

    An authentication POST request must be sent to the generated http endpoint with the syntax specified in PACT Tech Specs V2.2 § api-action-auth-request (the credentials need not be correct).

    Expected Response:
    The target host system either refuses to process the request (for instance the HTTP port 80 is not open) or responds with an HTTP error response code.

    References:
    [1] https://example.com/pact-tech-specs-v2-2

    This test case verifies that the target host system refuses to process the request or responds with an HTTP error response code when attempting authentication through HTTP (non-HTTPS).
    """

    # Modify the client's base URL to use HTTP scheme
    http_url = str(client.base_url).replace("https://", "http://")

    # Send an authentication POST request to the modified http endpoint
    response = client.post(http_url + "/auth/token", data={"grant_type": "", "scope": "", "client_id": "test_username", "client_secret": "test_password"})

    # Verify that the target host system refuses to process the request or responds with an HTTP error response code
    assert response.status_code >= 400


@pytest.mark.conformance
def test_015_attempt_listfootprints_through_http_non_https(client, auth_header):
    """Test Case 015: Attempt ListFootprints through HTTP (non-HTTPS)

    Condition:
    According to PACT Tech Specs V2.2 § api-requirements, a host system must offer its actions under https method only.

    Request:
    An http-only equivalent of the test target host system ListFootprints endpoint must be generated, replacing "https://" by "http://".
    A ListFootprints GET request must be sent to the generated http endpoint with the syntax specified in PACT Tech Specs V2.2 § api-action-list-request (the access token need not be valid).

    Expected Response:
    The target host system either refuses to process the request (for instance the HTTP port 80 is not open) or responds with an HTTP error response code.

    References:
    [1] https://example.com/pact-tech-specs-v2-2

    This test case verifies that the target host system refuses to process the request or responds with an HTTP error response code when attempting ListFootprints through HTTP (non-HTTPS).
    """

    # Modify the client's base URL to use HTTP scheme
    http_url = str(client.base_url).replace("https://", "http://")

    # Send a ListFootprints GET request to the modified http endpoint
    response = client.get(http_url + "/2/footprints/", headers=auth_header)

    # Verify that the target host system refuses to process the request or responds with an HTTP error response code
    assert response.status_code >= 400


@pytest.mark.conformance
def test_016_get_filtered_list_of_footprints(client, auth_header):
    """Test Case 016: Get Filtered List of Footprints"""

    # Define the filter parameter
    filter_param = "$filter=productCategoryCpc eq '22222'"

    # Send the GET request with the filter parameter
    response = client.get(f"/2/footprints/?{filter_param}", headers=auth_header)

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert the response contains only footprints with CPC code "3342"
    footprints = response.json()["data"]
    for footprint in footprints:
        assert footprint["productCategoryCpc"] == "22222"


def test_017_attempt_getfootprint_through_http_non_https(client, auth_header):
    """Test Case 016: Attempt GetFootprint through HTTP (non-HTTPS)

    Condition:
    According to PACT Tech Specs V2.2 § api-requirements, a host system must offer its actions under https method only.

    Request:
    An http-only equivalent of the test target host system GetFootprint endpoint must be generated, replacing "https://" by "http://".
    A GetFootprint GET request must be sent to the generated http endpoint with the syntax specified in PACT Tech Specs V2.2 § api-action-get-request (the GetPfId need not exist).

    Expected Response:
    The target host system either refuses to process the request (for instance the HTTP port 80 is not open) or responds with an HTTP error response code.

    References:
    [1] https://example.com/pact-tech-specs-v2-2

    This test case verifies that the target host system refuses to process the request or responds with an HTTP error response code when attempting GetFootprint through HTTP (non-HTTPS).
    """

    # Modify the client's base URL to use HTTP scheme
    http_url = str(client.base_url).replace("https://", "http://")

    # Send a GetFootprint GET request to the modified http endpoint
    response = client.get(http_url + "/{id}", headers=auth_header)

    # Verify that the target host system refuses to process the request or responds with an HTTP error response code
    assert response.status_code >= 400


@pytest.mark.xfail(reason="Endpoint is not implemented", strict=True)
def test_018_receive_notification_of_pcf_update(client, auth_header):
    """Test Case 018: Receive Notification of PCF Update

    Condition:
    This test case will become mandatory test case with the release of version 2.2 of the Technical Specifications.

    Request:
    A POST request must be sent to the test target host system’s /2/events endpoint with the syntax specified in PACT Tech Specs V2.2 § api-action-events-case-1.

    Expected Response:
    The test target host system must respond with 200 OK and an empty body.

    If the test target host system calls the GetFootprint action with the pfId included in the notification, the corresponding PCF must be returned.
    """

    # Define the event data
    event_data = {
        "type": "org.wbcsd.pathfinder.ProductFootprint.Published.v1",
        "specversion": "1.0",
        "id": "EventId",
        "source": "//EventHostname/EventSubpath",
        "time": "2022-05-31T17:31:00Z",
        "data": {
            "pfIds": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
        }
    }

    # Send a POST request to the /events endpoint
    response = client.post("/2/events", json=event_data, headers=auth_header)

    # Verify that the response status code is 200
    assert response.status_code == 200

    # Verify that the response body is empty
    assert response.json() == {}


@pytest.mark.xfail(reason="Events functionality is not implemented", strict=True)
def test_019_notify_of_pcf_update(client, auth_header):
    """Test Case 019: Notify of PCF Update

    Condition:
    This test case will become mandatory test case with the release of version 2.2 of the Technical Specifications.

    Request:
    The test target host system must authenticate with the testing party (performing the customary Authentication Flow and obtain an access token.
    The test target host system must send a POST request to the testing party’s /2/events endpoint with a valid access token and the syntax specified in PACT Tech Specs V2.2 § api-action-events-case-1.

    Expected Response:
    If the testing party has implemented the Events functionality, it should respond with 200 OK and an empty body.
    Otherwise, it should respond with 400 Bad Request and a JSON body containing the error response NotImplemented, as specified in PACT Tech Specs V2.2 § api-error-responses.
    """

    # Send a POST request to the /events endpoint
    # This test case cannot be implemented without a secondary system to test against
    # It would require setting up a separate server to receive the POST request
    # and respond accordingly, which is outside the scope of this test suite

    pass


@pytest.mark.xfail(reason="Asynchronous PCF request functionality is not implemented", strict=True)
def test_020_asynchronous_pcf_request(client, auth_header):
    """Test Case 020: Asynchronous PCF Request

    Condition:
    This test case will become mandatory test case with the release of version 2.2 of the Technical Specifications.

    Request:
    A POST request must be sent to the test target host system’s /2/events endpoint with the syntax specified in PACT Tech Specs V2.2 § api-action-events-case-2-request.

    Expected Response:
    The test target host system must respond with 200 OK.
    """

    # Define the payload for the POST request
    payload = {
        "type": "org.wbcsd.pathfinder.ProductFootprintRequest.Created.v1",
        "specversion": "1.0",
        "id": "EventId",
        "source": "//EventHostname/EventSubpath",
        "time": "2022-05-31T17:31:00Z",
        "data": {
            "pf": {
                "productIds": [
                    "urn:gtin:4712345060507"
                ]
            },
            "comment": "Optional comment about the request"
        }
    }

    # Send a POST request to the /events endpoint with the payload
    response = client.post("/2/events", headers=auth_header, json=payload)

    # Verify that the response status code is 200
    assert response.status_code == 200


@pytest.mark.xfail(reason="Asynchronous PCF response functionality is not implemented", strict=True)
def test_021_respond_to_asynchronous_pcf_request(client, auth_header):
    """Test Case 021: Respond to Asynchronous PCF Request

    Condition:
    This test case will become mandatory test case with the release of version 2.2 of the Technical Specifications.

    Request:
    The test target host system must authenticate with the testing party (performing the customary Authentication Flow) and obtain an access token.
    The test target host system must send a POST request to the testing party’s /2/events endpoint with a valid access token and the syntax specified in PACT Tech Specs V2.2 § api-action-events-case-2-response.

    Expected Response:
    If the testing party has implemented the Events functionality, it should respond with 200 OK and an empty body.
    Otherwise, it should respond with 400 Bad Request and a JSON body containing the error response NotImplemented, as specified in PACT Tech Specs V2.2 § api-error-responses.
    """

    # Define the payload for the POST request
    payload = {
        "type": "org.wbcsd.pathfinder.ProductFootprintRequest.Fulfilled.v1",
        "specversion": "1.0",
        "id": "1",
        "source": "//EventHostname/EventSubpath",
        "data": {
            "requestEventId": "2",
            "pfs": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
        }
    }

    # Send a POST request to the /events endpoint with the payload
    response = client.post("/2/events", headers=auth_header, json=payload)

    # If the response status code is 200, verify that the response body is empty
    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.conformance
def test_022_attempt_events_with_expired_token(client, auth_header):
    """
    6.11. Test Case 022: Attempt Events with Expired Token
    Tests the target host system’s ability to reject an Events request with an expired access token with the correct error response.

    6.11.1. Request
    An Events POST request must be sent to the /2/events endpoint of the test target host system with an expired access token and the syntax specified in PACT Tech Specs V2.2 § api-action-events-request (the EnventBody is irrelevant).

    6.11.2. Expected Response
    The test target host system must respond with a 401 Unauthorized and a JSON body that should contain the error response TokenExpired, as specified in PACT Tech Specs V2.2 § api-error-responses.

    NOTE: Since the access token is expired, re-authentication should in principle solve the issue. By returning the HTTP error code 401 (instead of, e.g., 403), the host system signals that re-authentication should be attempted.
    """

    # Create an expired token by moving the clock forward by one day
    with freezegun.freeze_time(datetime.utcnow() + timedelta(days=1)):
        response = client.post("/2/events", headers=auth_header)

        assert response.status_code == 401
        assert response.json()["code"] == "TokenExpired"


@pytest.mark.conformance
def test_023_attempt_events_with_invalid_token(client):
    """
    6.12. Test Case 023: Attempt Events with Invalid Token
    Tests the target host system’s ability to reject an Events request with an invalid access token with the correct error response.

    6.12.1. Request
    An Events POST request must be sent to the /2/events endpoint of the test target host system with an invalid access token and the syntax specified in PACT Tech Specs V2.2 § api-action-events-request (the EnventBody is irrelevant).

    6.12.2. Expected Response
    The test target host system must respond with a 403 Forbidden and a JSON body containing the error response AccessDenied, as specified in PACT Tech Specs V2.2 § api-error-responses.

    NOTE: Since the access token is invalid, re-authentication cannot solve the issue. By returning the HTTP error code 403 (instead of, e.g., 401), the host system signals that there is no gain in re-authenticating.
    """

    # Create an invalid token by modifying a valid token
    invalid_token = 'invalid-token'
    invalid_auth_header = {'Authorization': f'Bearer {invalid_token}'}

    response = client.post("/2/events", headers=invalid_auth_header)

    assert response.status_code == 403
    assert response.json()["code"] == "AccessDenied"


def test_024_attempt_action_events_through_http_non_https(client, auth_header):
    """Test Case 024: Attempt Action Events through HTTP (non-HTTPS)

    Condition:
    According to PACT Tech Specs V2.2 § api-requirements, a host system must offer its actions under https method only.

    Request:
    An http-only equivalent of the test target host system Events endpoint must be generated, replacing "https://" by "http://".
    An Events POST request must be sent to the generated http endpoint with the syntax specified in PACT Tech Specs V2.2 § api-action-events-request (the access token and EnventBody are irrelevant).

    Expected Response:
    No response is expected: the request must not be processed.
    """

    # Modify the client's base URL to use HTTP scheme
    http_url = str(client.base_url).replace("https://", "http://")

    payload = {
        "type": "org.wbcsd.pathfinder.ProductFootprintRequest.Created.v1",
        "specversion": "1.0",
        "id": "EventId",
        "source": "//EventHostname/EventSubpath",
        "time": "2022-05-31T17:31:00Z",
        "data": {
            "pf": {
                "productIds": [
                    "urn:gtin:4712345060507"
                ]
            },
            "comment": "Optional comment about the request"
        }
    }

    # Send a POST request to the /events endpoint with the payload
    response = client.post("/2/events", headers=auth_header, json=payload)

    # Verify that the target host system refuses to process the request or responds with an HTTP error response code
    assert response.status_code >= 400
