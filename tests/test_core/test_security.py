import pytest
from datetime import timedelta, datetime

import freezegun
from jose import jwt
from jose.exceptions import JWSError, ExpiredSignatureError

from core.config import settings
from core.security import create_access_token


@pytest.fixture()
def test_data():
    return {"sub": "testuser@example.com"}


@pytest.fixture()
def test_expiration_time():
    return timedelta(minutes=15)


def test_create_access_token_success(test_data, test_expiration_time):
    token = create_access_token(data=test_data, expires_delta=test_expiration_time)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert payload.get("sub") == test_data["sub"]
    assert payload.get("exp")


def test_create_access_token_missing_secret_key(test_data, monkeypatch):
    monkeypatch.setattr(settings, "SECRET_KEY", None)
    with pytest.raises(JWSError):
        create_access_token(data=test_data)


def test_create_access_token_invalid_algorithm(test_data, monkeypatch):
    monkeypatch.setattr(settings, "ALGORITHM", "InvalidAlgorithm")
    with pytest.raises(JWSError):
        create_access_token(data=test_data)


def test_token_expiration(test_data):
    expires_delta: timedelta = timedelta(seconds=5)
    token: str = create_access_token(test_data, expires_delta)

    # Decode the token immediately - should be valid
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get("sub") == test_data["sub"]

    # Wait for the token to expire
    with freezegun.freeze_time(datetime.utcnow() + expires_delta + timedelta(seconds=1)):
        with pytest.raises(ExpiredSignatureError):
            jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
