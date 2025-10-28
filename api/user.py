from typing import Annotated

from fastapi import APIRouter, Depends

from core.dependencies import get_user_service, UserService
from schemas.requests import CreateUserRequest
from schemas.responses import SuccessResponse, UserResponse

router = APIRouter(prefix="/organizations", tags=["users"])


@router.post("/{org_id}/users/", response_model=SuccessResponse)
async def create_user(
    org_id: str,
    request: CreateUserRequest,
    service: Annotated[UserService, Depends(get_user_service)],
):
    user = await service.create_user(
        email=request.email,
        password=request.password,
        org_id=org_id,
        role=request.role,
    )

    return SuccessResponse(
        data=UserResponse(
            id=str(user.id),
            email=user.email,
            org_id=user.org_id,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        ),
        message="User created successfully",
    )
