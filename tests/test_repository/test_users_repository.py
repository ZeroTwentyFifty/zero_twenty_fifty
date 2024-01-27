import pytest

from core.hashing import Hasher
from db.models.user import User
from db.repository.users import create_new_user
from schemas.user import UserCreate


@pytest.fixture(scope="function")
def test_fixture_user(db_session):
    user_data = {"username": "testuser", "email": "testuser@example.com", "password": "testuser"}
    user = create_new_user(user=UserCreate(**user_data), db=db_session)
    return user


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
