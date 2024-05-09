from fastapi import FastAPI
from authx import AuthX, AuthXConfig
from datetime import timedelta

from core.config import settings


def get_authx_security() -> AuthX:
    """
    Creates and configures an AuthX instance for use in FastAPI dependencies.

    Returns:
        AuthX: The configured AuthX instance.
    """
    config = AuthXConfig()
    config.JWT_SECRET_KEY = settings.SECRET_KEY
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)
    security = AuthX(config=config)
    return security


def apply_authx_error_handling(app: FastAPI):
    """
    Applies AuthX error handling to a FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    security = get_authx_security()
    security.handle_errors(app)
