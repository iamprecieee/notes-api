from models.organization import Organization
from core.exceptions import NotFoundError


class OrganizationService:
    async def create_organization(self, name: str) -> Organization:
        org = Organization(name=name)
        await org.insert()
        return org
