import pytest

from db.repository.login import get_user


def test_get_user_by_username_success(db_session, test_user):
    retrieved_user = get_user(username='testuser@example.com', db=db_session)
    assert retrieved_user == test_user


def test_get_user_by_username_failure(db_session):
    retrieved_user = get_user(username='non_existent_user@example.com', db=db_session)
    assert retrieved_user is None
