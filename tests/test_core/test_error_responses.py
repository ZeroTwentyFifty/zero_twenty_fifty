import json

from core.error_responses import (
    AccessDeniedError, BadRequestError, NoSuchFootprintError,
    NotImplementedError, TokenExpiredError, InternalError, DuplicateEntryError
)


def test_access_denied_error():
    error = AccessDeniedError()
    assert error.message == "Access denied"
    assert error.code == "AccessDenied"
    assert error.status_code == 403


def test_bad_request_error():
    error = BadRequestError()
    assert error.message == "Bad Request"
    assert error.code == "BadRequest"
    assert error.status_code == 400


def test_no_such_footprint_error():
    error = NoSuchFootprintError()
    assert error.message == "The specified footprint does not exist"
    assert error.code == "NoSuchFootprint"
    assert error.status_code == 404


def test_not_implemented_error():
    error = NotImplementedError()
    assert error.message == "The specified Action or header you provided implies functionality that is not implemented"
    assert error.code == "NotImplemented"
    assert error.status_code == 400


def test_token_expired_error():
    error = TokenExpiredError()
    assert error.message == "The specified access token has expired"
    assert error.code == "TokenExpired"
    assert error.status_code == 401


def test_internal_error():
    error = InternalError()
    assert error.message == "An internal or unexpected error has occurred"
    assert error.code == "InternalError"
    assert error.status_code == 500


def test_duplicate_entry_error():
    error = DuplicateEntryError("A user with this email already exists")
    assert error.message == "A user with this email already exists"
    assert error.code == "DuplicateEntry"
    assert error.status_code == 409


def test_error_response_to_json_response():
    error = NoSuchFootprintError()
    json_response = error.to_json_response()
    assert json.loads(json_response.body.decode("utf-8"))["message"] == error.message
    assert json.loads(json_response.body.decode("utf-8"))["code"] == error.code
    assert json_response.status_code == error.status_code
