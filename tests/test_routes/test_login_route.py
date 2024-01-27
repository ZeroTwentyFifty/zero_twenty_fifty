import json
from datetime import timedelta

from fastapi import HTTPException
from fastapi.responses import JSONResponse
import pytest

from apis.version1.route_login import authenticate_user, get_current_user_from_token
from core.security import create_access_token


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


def test_get_current_user_from_token_success(client, test_user, test_credentials, db_session):
    username, password = test_credentials

    access_token = create_access_token(data={"sub": test_user.email})

    user = get_current_user_from_token(token=access_token, db=db_session)

    assert user == test_user
    assert user.email == username # needs to be touched up a bit here


def test_get_current_user_from_token_failure_with_invalid_token(client, test_user, test_credentials, db_session):
    access_token = "InvalidToken"
    with pytest.raises(HTTPException) as exc_info:
        get_current_user_from_token(token=access_token, db=db_session)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "AccessDenied OAuth2 Client Credentials"
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


def test_get_current_user_from_token_failure_with_invalid_token_json_response(client, test_user, test_credentials, db_session):
    access_token = create_access_token(data={"sub": ""})
    response = get_current_user_from_token(token=access_token, db=db_session)
    json_response = json.loads(response.body)
    assert isinstance(response, JSONResponse)
    assert response.status_code == 403
    assert json_response == {'message': 'Access Denied', 'code': 'AccessDenied'}
    assert json_response["message"] == "Access Denied"
    assert json_response["code"] == "AccessDenied"


def test_get_current_user_from_token_failure_with_expired_token(client, test_user, test_credentials, db_session):
    access_token = create_access_token(data={"sub": test_user.email}, expires_delta=timedelta(minutes=-1))
    response = get_current_user_from_token(token=access_token, db=db_session)
    json_response = json.loads(response.body)
    assert isinstance(response, JSONResponse)
    assert response.status_code == 401
    assert json_response == {"message":"The specified access token has expired","code":"TokenExpired"}
    assert json_response["message"] == "The specified access token has expired"
    assert json_response["code"] == "TokenExpired"
