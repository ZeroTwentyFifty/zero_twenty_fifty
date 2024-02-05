import pytest
from fastapi import HTTPException

from core.exceptions import (
    AccessDeniedException,
    BadRequestException,
    NoSuchFootprintException,
    NotImplementedException,
    TokenExpiredException,
    InternalErrorException,
)


def test_access_denied_exception():
    with pytest.raises(AccessDeniedException) as exc_info:
        raise AccessDeniedException()

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Access denied"


def test_bad_request_exception():
    with pytest.raises(BadRequestException) as exc_info:
        raise BadRequestException()

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Bad Request"


def test_no_such_footprint_exception():
    with pytest.raises(NoSuchFootprintException) as exc_info:
        raise NoSuchFootprintException()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "The specified footprint does not exist"


def test_not_implemented_exception():
    with pytest.raises(NotImplementedException) as exc_info:
        raise NotImplementedException()

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == (
        "The specified Action or header you provided implies "
        "functionality that is not implemented"
    )


def test_token_expired_exception():
    with pytest.raises(TokenExpiredException) as exc_info:
        raise TokenExpiredException()

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "The specified access token has expired"


def test_internal_error_exception():
    with pytest.raises(InternalErrorException) as exc_info:
        raise InternalErrorException()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "An internal or unexpected error has occurred"


def test_exception_module_inheritance():
    """
    Only implemented for one of our custom implemented Exception classes
    due to the unlikeliness of implementation drift for only one exception class,
    if one of them stop inheriting from there, probably all of them will, and thus
    this test will break.
    """
    assert issubclass(AccessDeniedException, HTTPException)
