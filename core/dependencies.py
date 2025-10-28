from fastapi import Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from core.exceptions import AuthenticationError
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
    request: Request,
) -> CurrentUser:
    if not hasattr(request.state, "user") or request.state.user is None:
        raise AuthenticationError(detail="Authentication required")

    return CurrentUser(**request.state.user)


def get_organization_service() -> OrganizationService:
    return OrganizationService()


def get_user_service() -> UserService:
    return UserService()


def get_auth_service() -> AuthService:
    return AuthService()


def get_note_service() -> NoteService:
    return NoteService()
