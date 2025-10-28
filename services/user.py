from models.user import User
from models.organization import Organization
from core.security import hash_password
from core.exceptions import ForbiddenError, NotFoundError, ConflictError
from core.config import get_settings


class UserService:
    async def create_user(
        self, email: str, password: str, org_id: str, role: str
    ) -> User:
        settings = get_settings()

        org = await Organization.get(org_id)
        if not org:
            raise NotFoundError(status_code=404, detail="Organization not found")

        existing_user = await User.find_one(User.email == email, User.org_id == org_id)
        if existing_user:
            raise ConflictError(
                status_code=409, detail="Email already exists in this organization"
            )

        if len(password) < settings.min_password_length:
            raise ValueError(
                f"Password must be at least {settings.min_password_length} characters"
            )

        if role not in ["reader", "writer", "admin"]:
            raise ValueError("Invalid role. Must be reader, writer, or admin")

        user_count = await User.find(User.org_id == org_id).count()

        if user_count == 0:
            role = "admin"
        elif role == "admin":
            raise ForbiddenError(
                status_code=403, detail="Cannot self-assign admin role"
            )

        hashed_password = hash_password(password)
        user = User(
            email=email,
            password=hashed_password,
            org_id=org_id,
            role=role,
        )
        await user.insert()
        return user

    async def get_user_by_id(self, user_id: str) -> User:
        user = await User.get(user_id)
        if not user:
            raise NotFoundError(status_code=404, detail="User not found")
        return user
