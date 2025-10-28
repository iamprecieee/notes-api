from fastapi import HTTPException


class AuthenticationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class NotFoundError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)


class ForbiddenError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=403, detail=detail)


class ConflictError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)


class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
