from typing import Annotated

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from pydantic import BaseModel

from core.exceptions import AuthenticationError
from core.security import decode_access_token
from services.auth import AuthService
from services.note import NoteService
from services.organization import OrganizationService
from services.user import UserService

security = HTTPBearer()


class CurrentUser(BaseModel):
    id: str
    org_id: str
    role: str
    email: str


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> CurrentUser:
    try:
        token = credentials.credentials
        payload = decode_access_token(token)

        return CurrentUser(
            id=payload["user_id"],
            org_id=payload["org_id"],
            role=payload["role"],
            email=payload["email"],
        )
    except JWTError:
        raise AuthenticationError(
            status_code=401,
            detail="Invalid authentication token",
        )
    except KeyError:
        raise AuthenticationError(
            status_code=401,
            detail="Invalid token payload",
        )


def get_organization_service() -> OrganizationService:
    return OrganizationService()


def get_user_service() -> UserService:
    return UserService()


def get_auth_service() -> AuthService:
    return AuthService()


def get_note_service() -> NoteService:
    return NoteService()
