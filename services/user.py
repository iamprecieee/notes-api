from models.user import User
from models.organization import Organization
from core.security import hash_password
from core.exceptions import ForbiddenError, NotFoundError, ConflictError
from pymongo.errors import DuplicateKeyError


class UserService:
    async def create_user(
        self, email: str, password: str, org_id: str, role: str
    ) -> User:
        org = await Organization.get(org_id)
        if not org:
            raise NotFoundError(detail="Organization not found")

        user_count = await User.find(User.org_id == org_id).count()

        if user_count == 0:
            role = "admin"
        elif role == "admin":
            raise ForbiddenError(detail="Cannot self-assign admin role")

        hashed_password = hash_password(password)

        user = User(
            email=email,
            password=hashed_password,
            org_id=org_id,
            role=role,
        )

        try:
            await user.insert()
        except DuplicateKeyError:
            raise ConflictError(detail="Email already exists in this organization")

        return user
