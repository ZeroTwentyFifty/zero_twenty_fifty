from authx.exceptions import JWTDecodeError, MissingTokenError
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import add_pagination
from fastapi.responses import JSONResponse

from apis.base import api_router
from core.auth_config import apply_authx_error_handling
from core.config import settings
from core.pagination import PaginationMiddleware


from core.app_config import create_app

app = create_app()