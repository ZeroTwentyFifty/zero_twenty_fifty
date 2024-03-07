def test_get_events(client, auth_header):
    response = client.post(
        url="/events",
        headers=auth_header
    )

    assert response.status_code == 400
    assert response.json() == {
        "message": "The specified Action or header you provided implies functionality that is not implemented",
        "code": "NotImplemented"
    }


def test_get_events_unauthenticated(client):
    response = client.post("/events")

    assert response.status_code == 403
    assert "AccessDenied" in response.text
