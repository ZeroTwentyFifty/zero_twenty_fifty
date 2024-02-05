from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine
from core.pagination import PaginationMiddleware
from fastapi import FastAPI, Request, Header, status
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder


def include_router(app):
    app.include_router(api_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    create_tables()
    add_pagination(app)
    return app


app = start_application()

app.add_middleware(PaginationMiddleware)


@app.exception_handler(RequestValidationError)
def standard_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.exception_handler(RequestValidationError)
def custom_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path == '/auth/token':
        return JSONResponse({"message": "Access Denied", "code": "AccessDenied"}, status_code=403)
    else:
        return standard_validation_exception_handler(request, exc)


@app.exception_handler(HTTPException)
def custom_oauth2_access_denied_handler(request: Request, exc: HTTPException):
    if exc.detail == "AccessDenied OAuth2 Client Credentials":
        return JSONResponse({"message": "Access Denied", "code": "AccessDenied"}, status_code=403)
