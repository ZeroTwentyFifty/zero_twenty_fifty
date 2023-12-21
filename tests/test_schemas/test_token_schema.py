import datetime

from schemas.token import Token
import pytest

def test_token_schema_validation():
    """Test successful validation for valid token data."""
    token_data = {
        "access_token": "some_access_token",
        "token_type": "bearer"
    }
    token = Token(**token_data)
    assert token.access_token == token_data["access_token"]
    assert token.token_type == token_data["token_type"]

def test_token_schema_missing_access_token():
    """Test validation error for missing access_token."""
    invalid_data = {
        "token_type": "bearer"
    }
    with pytest.raises(ValueError):
        Token(**invalid_data)

def test_token_schema_invalid_token_type():
    """Test validation error for invalid token_type."""
    invalid_data = {
        "access_token": "some_access_token",
        "token_type": datetime.datetime.now()
    }
    with pytest.raises(ValueError):
        Token(**invalid_data)
