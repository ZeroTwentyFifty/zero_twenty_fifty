import pytest
from sqlalchemy.exc import IntegrityError

from db.models.user import User


def test_user_creation(test_user):
    assert test_user.id is not None
    assert test_user.username == "testuser"
    assert test_user.email == "testuser@example.com"
    assert test_user.is_active is True
    assert test_user.is_superuser is False


def test_user_uniqueness(db_session):
    user1 = User(username="user1", email="user1@example.com", hashed_password="password")
    db_session.add(user1)
    db_session.commit()

    with pytest.raises(IntegrityError):
        user2 = User(username="user1", email="user2@example.com", hashed_password="password")
        db_session.add(user2)
        db_session.commit()
