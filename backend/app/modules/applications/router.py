import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import AuthUser, get_current_user
from app.database.database import get_db
from app.database.models.application import StudentApplication, ApplicationStatusHistory
from datetime import datetime, timezone

router = APIRouter()

class CreateApplicationRequest(BaseModel):
    scheme_id: uuid.UUID

class UpdateApplicationRequest(BaseModel):
    status: str
    notes: Optional[str] = None

@router.get("/applications/me")
async def get_my_applications(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    result = await db.execute(
        select(StudentApplication).where(
            StudentApplication.student_id == uuid.UUID(current_user.user_id)
        )
    )
    apps = result.scalars().all()
    return [{"id": str(a.id), "scheme_id": str(a.scheme_id), "status": a.status} for a in apps]

@router.post("/applications", status_code=201)
async def create_application(
    data: CreateApplicationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    app = StudentApplication(
        student_id=uuid.UUID(current_user.user_id),
        scheme_id=data.scheme_id,
        status="planning",
    )
    db.add(app)
    await db.flush()
    return {"application_id": str(app.id), "status": "planning"}

@router.patch("/applications/{application_id}")
async def update_application(
    application_id: uuid.UUID,
    data: UpdateApplicationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    result = await db.execute(
        select(StudentApplication).where(
            StudentApplication.id == application_id,
            StudentApplication.student_id == uuid.UUID(current_user.user_id),
        )
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    history = ApplicationStatusHistory(
        application_id=app.id,
        old_status=app.status,
        new_status=data.status,
        changed_by=uuid.UUID(current_user.user_id),
        note=data.notes,
    )
    db.add(history)
    app.status = data.status
    if data.notes:
        app.notes = data.notes
    await db.flush()
    return {"application_id": str(app.id), "new_status": app.status}
