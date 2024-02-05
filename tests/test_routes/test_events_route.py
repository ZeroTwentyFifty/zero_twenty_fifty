import pytest


@pytest.fixture
def access_token(client, test_user):
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


def test_get_events(client, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/events", headers=headers)

    assert response.status_code == 400
    assert response.json() == {
        "message": "The specified Action or header you provided implies functionality that is not implemented",
        "code": "NotImplemented"
    }
