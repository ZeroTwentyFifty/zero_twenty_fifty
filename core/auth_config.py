from fastapi import Depends
from authx import AuthX, AuthXConfig, TokenPayload
from datetime import timedelta

from core.config import settings # Assuming your SECRET_KEY is in a settings file

def get_authx_security():
    config = AuthXConfig()
    config.JWT_SECRET_KEY = settings.SECRET_KEY
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)
    security = AuthX(config=config)
    return security

# Optionally add this if you used security.handle_errors(app) in main.py:
def apply_authx_error_handling(app):
    security = get_authx_security()
    security.handle_errors(app)