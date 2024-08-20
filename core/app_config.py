from authx.exceptions import JWTDecodeError, MissingTokenError
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi.responses import JSONResponse

from apis.base import api_router
from core.auth_config import apply_authx_error_handling
from core.config import settings
from core.pagination import PaginationMiddleware

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.include_router(api_router)
    add_pagination(app)
    app.add_middleware(PaginationMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    apply_authx_error_handling(app)

    @app.exception_handler(MissingTokenError)
    async def missing_bearer_token_error_handler(request, exc):
        return JSONResponse({"message": "Bad Request", "code": "BadRequest"}, status_code=400)

    @app.exception_handler(JWTDecodeError)
    async def jwt_decode_error_handler(request, exc):
        decode_error_reason: str = exc.args[0]
        if decode_error_reason == "Signature has expired":
            return JSONResponse({"message": "The specified access token has expired", "code": "TokenExpired"},
                                status_code=401)
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

    return app
