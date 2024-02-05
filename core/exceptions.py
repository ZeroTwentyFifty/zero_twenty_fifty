from fastapi import HTTPException


class AccessDeniedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Access denied")


class BadRequestException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Bad Request")


class NoSuchFootprintException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="The specified footprint does not exist")


class NotImplementedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="The specified Action or header you provided implies functionality that is not implemented"
        )


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="The specified access token has expired")


class InternalErrorException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="An internal or unexpected error has occurred")
