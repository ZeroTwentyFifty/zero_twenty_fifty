from datetime import datetime
from datetime import timedelta
from typing import Optional

from jose import jwt

from core.config import settings


def create_access_token(*, data: dict[str, str]) -> str:
    """
    Generates a JWT access token containing the provided data.

    Args:
        data (dict): The data to be encoded in the token. This typically
            includes the user's identifier (e.g., "sub").

    Returns:
        str: The encoded JWT access token.

    Raises:
        JWSError: If an error occurs during JWT encoding.
    """

    print("Creating access token with data:", data)

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    print("Token will expire at:", expire)

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print("Encoded JWT:", encoded_jwt)

    return encoded_jwt
