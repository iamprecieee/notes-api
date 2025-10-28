from models.organization import Organization
from core.exceptions import NotFoundError


class OrganizationService:
    async def create_organization(self, name: str) -> Organization:
        org = Organization(name=name)
        await org.insert()
        return org

    async def get_organization(self, org_id: str) -> Organization:
        org = await Organization.get(org_id)
        if not org:
            raise NotFoundError(status_code=404, detail="Organization not found")
        return org
