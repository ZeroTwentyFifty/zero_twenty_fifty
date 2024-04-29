from fastapi.responses import JSONResponse

"""
Module for error responses.

Error responses are specified in detail such that data recipients can understand the cause of the error, and so that potentially host systems can react on and resolve errors automatically.

Each error response is a JSON object with the following properties:
    - code: a error response code encoded as a String
    - message: a error message encoded as a String

The error response codes and their related HTTP status codes are as follows:
    - AccessDenied: 403
    - BadRequest: 400
    - NoSuchFootprint: 404
    - NotImplemented: 400
    - TokenExpired: 401
    - InternalError: 500

A host system MAY return error messages different from the table below, for instance localized values depending on a data recipient.
"""


class ErrorResponse:
    """
    Base class for error responses.

    Attributes:
        message (str): A human-readable error description.
        code (str): An error response code.
        status_code (int): The HTTP status code associated with the error response code.
    """

    def __init__(self, message, code, status_code):
        self.message = message
        self.code = code
        self.status_code = status_code

    def to_json_response(self):
        """
        Returns a JSON response object with the error message and code.

        Returns:
            JSONResponse: A JSON response object with the error message and code.
        """
        return JSONResponse({"message": self.message, "code": self.code}, status_code=self.status_code)


class AccessDeniedError(ErrorResponse):
    """
    Error response for access denied errors.

    Attributes:
        message (str): A human-readable error description. Defaults to "Access denied".
        code (str): An error response code. Defaults to "AccessDenied".
        status_code (int): The HTTP status code associated with the error response code. Defaults to 403.
    """

    def __init__(self):
        super().__init__("Access denied", "AccessDenied", 403)


class BadRequestError(ErrorResponse):
    """
    Error response for bad request errors.

    Attributes:
        message (str): A human-readable error description. Defaults to "Bad Request".
        code (str): An error response code. Defaults to "BadRequest".
        status_code (int): The HTTP status code associated with the error response code. Defaults to 400.
    """

    def __init__(self):
        super().__init__("Bad Request", "BadRequest", 400)


class NoSuchFootprintError(ErrorResponse):
    """
    Error response for no such footprint errors.

    Attributes:
        message (str): A human-readable error description. Defaults to "The specified footprint does not exist".
        code (str): An error response code. Defaults to "NoSuchFootprint".
        status_code (int): The HTTP status code associated with the error response code. Defaults to 404.
    """

    def __init__(self):
        super().__init__("The specified footprint does not exist", "NoSuchFootprint", 404)


class NotImplementedError(ErrorResponse):
    """
    Error response for not implemented errors.

    Attributes:
        message (str): A human-readable error description. Defaults to "The specified Action or header you provided implies functionality that is not implemented".
        code (str): An error response code. Defaults to "NotImplemented".
        status_code (int): The HTTP status code associated with the error response code. Defaults to 400.
    """

    def __init__(self):
        super().__init__("The specified Action or header you provided implies functionality that is not implemented", "NotImplemented", 400)


class TokenExpiredError(ErrorResponse):
    """
    Error response for token expired errors.

    Attributes:
        message (str): A human-readable error description. Defaults to "The specified access token has expired".
        code (str): An error response code. Defaults to "TokenExpired".
        status_code (int): The HTTP status code associated with the error response code. Defaults to 401.
    """

    def __init__(self):
        super().__init__("The specified access token has expired", "TokenExpired", 401)


class InternalError(ErrorResponse):
    """
    Error response for internal errors.

    Attributes:
        message (str): A human-readable error description. Defaults to "An internal or unexpected error has occurred".
        code (str): An error response code. Defaults to "InternalError".
        status_code (int): The HTTP status code associated with the error response code. Defaults to 500.
    """

    def __init__(self):
        super().__init__("An internal or unexpected error has occurred", "InternalError", 500)