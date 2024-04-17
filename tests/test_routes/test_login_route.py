import json
from datetime import timedelta, datetime

import freezegun
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import pytest

from apis.version1.route_login import authenticate_user


@pytest.fixture
def test_credentials():
    return ("testuser@example.com", "testuser")


# TODO: Maybe this is failing due to some of the HTTP/HTTPS code that I have added, as it's blanket denying
# but it works fine on the hosted version which actually is HTTPS, when I run the other tests using the conformance-test
# tool (the ones targeting HTTP), they also fail on the online version, with a 403, which is what is being returned.
# You can see these in main.py
# TODO UPDATE: This is false, it is that the client_id is matched on the email
# address field and in order for "module" scoped fixtures to be available or run
# within a seprate module, they need to be atually called, I need to suss out how
# to use the autouse feature.
def test_login_for_access_token_success(client, test_user, test_credentials):
    """Test successful login with valid credentials."""
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


def test_login_for_access_token_failure(client):
    """Test failed login with invalid credentials."""
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

    assert response.status_code == 403
    assert response.json()["message"] == "Access Denied"
    assert response.json()["code"] == "AccessDenied"


def test_authenticate_user_success(client, test_user, test_credentials, db_session):
    """Test successful authentication with valid credentials."""
    username, password = test_credentials

    user = authenticate_user(username, password, db_session)

    assert user == test_user
