import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import AuthUser, get_current_user
from app.database.database import get_db
from app.database.models.user import UserProfile

router = APIRouter()

class UserMeResponse(BaseModel):
    id: str
    email: Optional[str]
    app_role: str
    full_name: str
    preferred_language: str
    model_config = {"from_attributes": True}

@router.get("/users/me")
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    result = await db.execute(
        select(UserProfile).where(UserProfile.id == uuid.UUID(current_user.user_id))
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "id": str(profile.id),
        "email": profile.email,
        "app_role": profile.app_role,
        "full_name": profile.full_name,
        "preferred_language": profile.preferred_language,
    }
