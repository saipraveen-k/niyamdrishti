"""
Security utilities: JWT validation, password hashing, Supabase auth.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)


class AuthUser:
    """Represents an authenticated user extracted from a Supabase JWT."""

    def __init__(
        self,
        user_id: str,
        email: Optional[str],
        role: str,
        app_role: str,
    ):
        self.user_id = user_id
        self.email = email
        self.role = role  # Supabase role (authenticated, anon, service_role)
        self.app_role = app_role  # NiyamDrishti role from user_metadata


async def verify_supabase_token(token: str) -> dict:
    """
    Verify a Supabase JWT by calling the Supabase /auth/v1/user endpoint.
    Returns the user data dict or raises HTTPException.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.supabase_url}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.supabase_anon_key,
            },
            timeout=10.0,
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return resp.json()


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> AuthUser:
    """
    FastAPI dependency: validates Bearer token and returns AuthUser.
    Raises 401 if missing or invalid.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    token = credentials.credentials
    user_data = await verify_supabase_token(token)

    app_role = (user_data.get("user_metadata") or {}).get("app_role", "student")

    return AuthUser(
        user_id=user_data["id"],
        email=user_data.get("email"),
        role=user_data.get("role", "authenticated"),
        app_role=app_role,
    )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Optional[AuthUser]:
    """
    Like get_current_user but returns None instead of raising for public endpoints.
    """
    if not credentials or not credentials.credentials:
        return None
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


class RoleChecker:
    """Dependency factory for role-based access control."""

    ROLE_HIERARCHY = {
        "student": 1,
        "college_coordinator": 2,
        "document_reviewer": 3,
        "admin": 4,
        "super_admin": 5,
    }

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if current_user.app_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.app_role}' is not permitted for this action",
            )
        return current_user


def require_roles(*roles: str):
    """Shorthand: require_roles('admin', 'super_admin')"""
    return RoleChecker(list(roles))


def require_self_or_roles(user_id_param: str, *roles: str):
    """
    Allow access if the authenticated user's ID matches the path param,
    OR if they have one of the given roles.
    """

    async def dependency(
        request: Request,
        current_user: AuthUser = Depends(get_current_user),
    ) -> AuthUser:
        path_user_id = request.path_params.get(user_id_param)
        if str(current_user.user_id) == str(path_user_id):
            return current_user
        if current_user.app_role in roles:
            return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return dependency
