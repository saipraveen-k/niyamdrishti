import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import AuthUser, get_current_user
from app.database.database import get_db
from app.database.models.user import StudentProfile

router = APIRouter()

class ProfileUpdateRequest(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    education_level: Optional[str] = None
    course_name: Optional[str] = None
    college_name: Optional[str] = None
    marks_percentage: Optional[float] = None
    cgpa: Optional[float] = None
    annual_family_income: Optional[int] = None
    caste_category: Optional[str] = None
    is_pwd: Optional[bool] = None

@router.get("/profiles/me")
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == uuid.UUID(current_user.user_id))
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return profile

@router.post("/profiles", status_code=201)
async def create_profile(
    data: ProfileUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    existing = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == uuid.UUID(current_user.user_id))
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Profile already exists")
    profile = StudentProfile(user_id=uuid.UUID(current_user.user_id), **data.model_dump(exclude_none=True))
    db.add(profile)
    await db.flush()
    return profile

@router.patch("/profiles/me")
async def update_my_profile(
    data: ProfileUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == uuid.UUID(current_user.user_id))
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    await db.flush()
    return profile
