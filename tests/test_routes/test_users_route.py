def test_create_user_by_superuser(client, superuser_auth_header):
    data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/users/", headers=superuser_auth_header, json=data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["is_active"] is True


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


def test_create_user_with_existing_email(client, superuser_auth_header, test_user):
    data = {"username": "newuser", "email": test_user.email, "password": "testpassword"}
    response = client.post("/users/", headers=superuser_auth_header, json=data)
    assert response.status_code == 409
    assert response.json()["message"] == "A user with this email already exists"
    assert response.json()["code"] == "DuplicateEntry"


def test_create_user_with_existing_username(client, superuser_auth_header, test_user):
    data = {"username": test_user.username, "email": "newuser@example.com", "password": "testpassword"}
    response = client.post("/users/", headers=superuser_auth_header, json=data)
    assert response.status_code == 409
    assert response.json()["message"] == "A user with this username already exists"
    assert response.json()["code"] == "DuplicateEntry"
