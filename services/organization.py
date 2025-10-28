from models.organization import Organization
from pymongo.errors import DuplicateKeyError
from core.exceptions import ConflictError


class OrganizationService:
    async def create_organization(self, name: str) -> Organization:
        org = Organization(name=name)

        try:
            await org.insert()
        except DuplicateKeyError:
            raise ConflictError(detail="Organization already exists with this name")

        return org
