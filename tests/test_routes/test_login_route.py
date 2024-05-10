import pytest


@pytest.fixture
def test_credentials():
    return "testuser@example.com", "testuser"


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

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_client"
    assert response.json()["error_description"] == "Authentication failed"


def test_login_for_access_token_valid_credentials(client, test_user, test_credentials):
    username, password = test_credentials
    response = client.post("/auth/token", data={"grant_type": "", "scope": "", "client_id": username, "client_secret": password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_for_access_token_invalid_credentials(client):
    test_username = "invalid_username"
    test_password = "invalid_password"
    response = client.post("/auth/token", data={"grant_type": "", "scope": "", "client_id": test_username, "client_secret": test_password})
    assert response.status_code == 400
    assert response.json()["error"] == "invalid_client"
    assert response.json()["error_description"] == "Authentication failed"
