from datetime import datetime
from datetime import timedelta
from typing import Optional

from jose import jwt

from core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generates a JWT access token containing the provided data.

    Args:
        data (dict): The data to be encoded in the token. This typically
            includes the user's identifier (e.g., "sub").
        expires_delta (Optional[timedelta], optional): The time after which
            the token should expire. If not provided, the default expiration
            time from `settings.ACCESS_TOKEN_EXPIRE_MINUTES` is used. Defaults to None.

    Returns:
        str: The encoded JWT access token.

    Raises:
        JWSError: If an error occurs during JWT encoding.

    TODO: Consider making `expires_delta` a more explicit duration
          parameter (e.g., `expires_in_minutes`) in the future to align
          with industry standards and reduce configuration complexity.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
