from typing import Annotated

from fastapi import APIRouter, Depends

from core.dependencies import get_organization_service, OrganizationService
from schemas.requests import CreateOrganizationRequest
from schemas.responses import SuccessResponse, OrganizationResponse

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("/", response_model=SuccessResponse)
async def create_organization(
    request: CreateOrganizationRequest,
    service: Annotated[OrganizationService, Depends(get_organization_service)],
):
    org = await service.create_organization(name=request.name)

    return SuccessResponse(
        data=OrganizationResponse(
            id=str(org.id),
            name=org.name,
            created_at=org.created_at,
        ),
        message="Organization created successfully",
    )
