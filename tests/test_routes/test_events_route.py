from datetime import timedelta, datetime

import freezegun


def test_get_events(client, auth_header):
    response = client.post(
        url="/2/events",
        headers=auth_header
    )

    assert response.status_code == 400
    assert response.json() == {
        "message": "The specified Action or header you provided implies functionality that is not implemented",
        "code": "NotImplemented"
    }


def test_get_events_with_expired_token(client, auth_header):
    with freezegun.freeze_time(datetime.utcnow() + timedelta(days=1)):
        response = client.post(
            url="/2/events",
            headers=auth_header
        )

        assert response.status_code == 401
        assert response.json() == {
            "message": "The specified access token has expired",
            "code": "TokenExpired"
        }


def test_get_events_unauthenticated(client):
    response = client.post("/2/events")

    assert response.status_code == 400
    assert response.json() == {
            "message": "Bad Request",
            "code": "BadRequest"
        }
