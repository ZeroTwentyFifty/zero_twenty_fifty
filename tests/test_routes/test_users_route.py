def test_create_user_by_superuser(client, superuser_auth_header):
    data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/users/", headers=superuser_auth_header, json=data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"


def test_create_user_no_auth(client):
    data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/users/", json=data)
    assert response.status_code == 400


def test_create_user_by_normal_user(client, auth_header):
    data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/users/", headers=auth_header, json=data)
    assert response.status_code == 403
    assert response.json()["code"] == "AccessDenied"


def test_create_user_with_invalid_data(client, auth_header):
    data = {"username": "", "email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/users/", headers=auth_header, json=data)
    assert response.status_code == 403
    assert response.json()["code"] == "AccessDenied"
