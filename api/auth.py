from typing import Annotated

from fastapi import APIRouter, Depends

from core.dependencies import get_auth_service, AuthService
from schemas.requests import LoginRequest
from schemas.responses import SuccessResponse, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=SuccessResponse)
async def login(
    request: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    access_token, user = await service.login(
        email=request.email,
        password=request.password,
    )

    return SuccessResponse(
        data=LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                org_id=user.org_id,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
            ),
        ),
        message="Login successful",
    )
