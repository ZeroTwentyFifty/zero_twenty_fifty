import pytest

from core.hashing import Hasher
from db.models.user import User
from db.repository.users import (
    create_new_user, create_new_superuser, retrieve_user,
    retrieve_user_by_email, retrieve_user_by_username, authenticate_user
)
from schemas.user import UserCreate


@pytest.fixture
def test_credentials():
    return "testuser@example.com", "testuser"


def test_create_new_user(db_session):
    user_data = {"username": "newuser", "email": "newuser@example.com", "password": "newuser"}
    user = create_new_user(user=UserCreate(**user_data), db=db_session)
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert user.is_active is True
    assert user.is_superuser is False


def test_create_new_user_invalid_email(db_session):
    user_data = {"username": "invaliduser", "email": "invalid_email", "password": "newuser"}
    with pytest.raises(ValueError):
        create_new_user(user=UserCreate(**user_data), db=db_session)


def test_create_new_user_commit(db_session):
    user_data = {"username": "newuser_commit", "email": "newuser_commit@example.com", "password": "newuser"}
    new_user = create_new_user(user=UserCreate(**user_data), db=db_session)
    db_session.commit()
    assert db_session.query(User).filter(User.username == "newuser_commit").first() is not None


def test_create_new_user_hashes_password(db_session, test_user):
    user_data = {"username": "newuser1", "email": "newuser1@example.com", "password": "newuser"}
    new_user = create_new_user(user=UserCreate(**user_data), db=db_session)
    assert new_user.hashed_password != user_data["password"]
    assert Hasher.verify_password(plain_password=user_data["password"], hashed_password=new_user.hashed_password)


def test_create_new_user_sets_attributes(db_session, test_user):
    user_data = {"username": "newuser2", "email": "newuser2@example.com", "password": "newuser"}
    new_user = create_new_user(user=UserCreate(**user_data), db=db_session)
    assert new_user.is_active is True
    assert new_user.is_superuser is False


def test_create_new_user_existing_email(db_session, test_user):
    user_data = {"username": "newuser", "email": test_user.email, "password": "newuser"}
    with pytest.raises(ValueError) as exc_info:
        create_new_user(user=UserCreate(**user_data), db=db_session)
    assert str(exc_info.value) == "A user with this email already exists"


def test_create_new_user_existing_username(db_session, test_user):
    user_data = {"username": test_user.username, "email": "newuser@example.com", "password": "newuser"}
    with pytest.raises(ValueError) as exc_info:
        create_new_user(user=UserCreate(**user_data), db=db_session)
    assert str(exc_info.value) == "A user with this username already exists"


def test_retrieve_user_not_found(db_session):
    item = retrieve_user(db=db_session, user_id=99999)
    assert item is None


def test_retrieve_user_success(test_user, db_session):
    item = retrieve_user(db=db_session, user_id=test_user.id)
    assert item is not None
    assert item.username == test_user.username
    assert item.email == test_user.email


@pytest.fixture(scope="function")
def test_superuser(db_session):
    user_data = {"username": "testsuperuser", "email": "testsuperuser@example.com", "password": "testsuperuser"}
    user = create_new_superuser(user=UserCreate(**user_data), db=db_session)
    return user


def test_create_new_superuser(db_session):
    user_data = {"username": "newsuperuser", "email": "newsuperuser@example.com", "password": "newsuperuser"}
    user = create_new_superuser(user=UserCreate(**user_data), db=db_session)
    assert user.username == "newsuperuser"
    assert user.email == "newsuperuser@example.com"
    assert user.is_active is True
    assert user.is_superuser is True


def test_create_new_superuser_invalid_email(db_session):
    user_data = {"username": "invalidsuperuser", "email": "invalid_email", "password": "newsuperuser"}
    with pytest.raises(ValueError):
        create_new_superuser(user=UserCreate(**user_data), db=db_session)


def test_create_new_superuser_commit(db_session):
    user_data = {"username": "newsuperuser_commit", "email": "newsuperuser_commit@example.com", "password": "newsuperuser"}
    new_user = create_new_superuser(user=UserCreate(**user_data), db=db_session)
    db_session.commit()
    assert db_session.query(User).filter(User.username == "newsuperuser_commit").first() is not None


def test_create_new_superuser_hashes_password(db_session, test_superuser):
    user_data = {"username": "newsuperuser1", "email": "newsuperuser1@example.com", "password": "newsuperuser"}
    new_user = create_new_superuser(user=UserCreate(**user_data), db=db_session)
    assert new_user.hashed_password != user_data["password"]
    assert Hasher.verify_password(plain_password=user_data["password"], hashed_password=new_user.hashed_password)


def test_create_new_superuser_sets_attributes(db_session, test_superuser):
    user_data = {"username": "newsuperuser2", "email": "newsuperuser2@example.com", "password": "newsuperuser"}
    new_user = create_new_superuser(user=UserCreate(**user_data), db=db_session)
    assert new_user.is_active is True
    assert new_user.is_superuser is True


def test_create_new_superuser_existing_email(db_session, test_superuser):
    user_data = {"username": "newsuperuser", "email": test_superuser.email, "password": "newsuperuser"}
    with pytest.raises(ValueError) as exc_info:
        create_new_superuser(user=UserCreate(**user_data), db=db_session)
    assert str(exc_info.value) == "A user with this email already exists"


def test_create_new_superuser_existing_username(db_session, test_superuser):
    user_data = {"username": test_superuser.username, "email": "newsuperuser@example.com", "password": "newsuperuser"}
    with pytest.raises(ValueError) as exc_info:
        create_new_superuser(user=UserCreate(**user_data), db=db_session)
    assert str(exc_info.value) == "A user with this username already exists"


def test_retrieve_user_by_email_not_found(db_session):
    item = retrieve_user_by_email(db=db_session, email="nonexistent@example.com")
    assert item is None


def test_retrieve_user_by_email_success(test_user, db_session):
    item = retrieve_user_by_email(db=db_session, email=test_user.email)
    assert item is not None
    assert item.username == test_user.username
    assert item.email == test_user.email


def test_retrieve_user_by_username_not_found(db_session):
    item = retrieve_user_by_username(db=db_session, username="nonexistent")
    assert item is None


def test_retrieve_user_by_username_success(test_user, db_session):
    item = retrieve_user_by_username(db=db_session, username=test_user.username)
    assert item is not None
    assert item.username == test_user.username
    assert item.email == test_user.email


def test_authenticate_user_valid_credentials(test_credentials, test_user, db_session):
    username, password = test_credentials
    authenticated_user = authenticate_user(username, password, db_session)
    assert authenticated_user == test_user


def test_authenticate_user_invalid_credentials(db_session):
    username = "testuser"
    password = "wrongpassword"
    authenticated_user = authenticate_user(username, password, db_session)
    assert authenticated_user is None


"""
TODO: We are not performing any sort of validation on the password field
    we need to improve this, at least add a minimum pw length check

def test_create_new_user_invalid_password(db_session):
    user_data = {"username": "invaliduser", "email": "invalid_password@example.com", "password": "t"}
    with pytest.raises(ValueError):
        create_new_user(user=UserCreate(**user_data), db=db_session)
"""
