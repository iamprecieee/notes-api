from fastapi import HTTPException


class AuthenticationError(HTTPException):
    pass


class NotFoundError(HTTPException):
    pass


class ForbiddenError(HTTPException):
    pass


class ConflictError(HTTPException):
    pass
