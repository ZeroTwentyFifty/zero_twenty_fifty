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


def test_create_access_token_success(test_data):
    token = create_access_token(data=test_data)
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


@pytest.mark.parametrize("expires_delta", [timedelta(minutes=35), timedelta(hours=2), timedelta(days=3)])
def test_token_expiration_success_with_default_expiration_setting_30_minutes(test_data, expires_delta):
    token = create_access_token(test_data)

    # Decode the token immediately - should be valid
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get("sub") == test_data["sub"]

    # Wait for the specified time and try to decode again
    with freezegun.freeze_time(datetime.utcnow() + expires_delta):
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


@pytest.mark.parametrize("expires_delta", [timedelta(minutes=61), timedelta(hours=2), timedelta(days=3)])
def test_token_expiration_success_with_changed_access_token_expire_minutes(test_data, monkeypatch, expires_delta):
    # Set a new expiration time for this test only
    monkeypatch.setattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60)

    token = create_access_token(test_data)

    # Decode the token immediately - should be valid
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get("sub") == test_data["sub"]

    # Wait for the specified time and try to decode again
    with freezegun.freeze_time(datetime.utcnow() + expires_delta):
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


@pytest.mark.parametrize("decode_time", [timedelta(seconds=30), timedelta(minutes=15), timedelta(minutes=29)])
def test_token_decode_success_with_default_expiration_setting_30_minutes(test_data, decode_time):
    token = create_access_token(test_data)

    with freezegun.freeze_time(datetime.utcnow() + decode_time):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload.get("sub") == test_data["sub"]


@pytest.mark.parametrize("decode_time", [timedelta(seconds=30), timedelta(minutes=15), timedelta(hours=1)])
def test_token_decode_success_with_changed_access_token_expire_minutes(test_data, monkeypatch, decode_time):
    monkeypatch.setattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60)

    token = create_access_token(test_data)

    with freezegun.freeze_time(datetime.utcnow() + decode_time):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload.get("sub") == test_data["sub"]
