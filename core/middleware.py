from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from core.security import decode_access_token


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/organizations/",
            "/auth/login",
        ]

        path = request.url.path
        is_public = path in public_paths or (
            path.startswith("/organizations/") and path.endswith("/users/")
        )

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                payload = decode_access_token(token)

                request.state.user = {
                    "id": payload["user_id"],
                    "org_id": payload["org_id"],
                    "role": payload["role"],
                    "email": payload["email"],
                }
            except JWTError:
                if not is_public:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "success": False,
                            "message": "Invalid authentication token",
                        },
                    )
            except KeyError:
                if not is_public:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"success": False, "message": "Invalid token payload"},
                    )
        else:
            if not is_public:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"success": False, "message": "Authentication required"},
                )

            request.state.user = None

        response = await call_next(request)
        return response
