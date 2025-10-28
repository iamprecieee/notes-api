from models.user import User
from core.security import verify_password, create_access_token
from core.exceptions import AuthenticationError


class AuthService:
    async def login(self, email: str, password: str) -> tuple[str, User]:
        user = await User.find_one(User.email == email)
        if not user:
            raise AuthenticationError(
                status_code=401, detail="Invalid email or password"
            )

        if not verify_password(password, user.password):
            raise AuthenticationError(
                status_code=401, detail="Invalid email or password"
            )

        if not user.is_active:
            raise AuthenticationError(
                status_code=401, detail="User account is inactive"
            )

        token_data = {
            "user_id": str(user.id),
            "org_id": user.org_id,
            "role": user.role,
            "email": user.email,
        }
        access_token = create_access_token(token_data)

        return access_token, user
