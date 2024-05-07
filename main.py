from datetime import timedelta

from authx import AuthX, AuthXConfig
from authx.exceptions import JWTDecodeError, MissingTokenError
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import add_pagination
from fastapi.responses import JSONResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


from apis.base import api_router
from core.config import settings
from core.pagination import PaginationMiddleware


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    add_pagination(app)
    return app


app = start_application()


@app.middleware("http")
async def https_only_middleware(request: Request, call_next):
    if not request.url.scheme == "https":
        return JSONResponse(status_code=405, content={"error": "Method Not Allowed"})

    response = await call_next(request)
    return response

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(PaginationMiddleware)

auth = AuthXConfig()
auth.JWT_SECRET_KEY = settings.SECRET_KEY
auth.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)
security = AuthX(config=auth)
security.handle_errors(app)


@app.exception_handler(MissingTokenError)
async def missing_bearer_token_error_handler(request, exc):
    return JSONResponse({"message": "Bad Request", "code": "BadRequest"}, status_code=400)


@app.exception_handler(JWTDecodeError)
async def jwt_decode_error_handler(request, exc):
    decode_error_reason: str = exc.args[0]
    if decode_error_reason == "Signature has expired":
        return JSONResponse({"message": "The specified access token has expired", "code": "TokenExpired"}, status_code=401)
    else:
        return JSONResponse(
            content={
                "message": "AccessDenied",
                "code": "AccessDenied"
            },
            status_code=403
        )


@app.exception_handler(RequestValidationError)
def standard_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
