import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import AuthUser, get_current_user
from app.database.database import get_db
from app.database.models.application import StudentImpact, StudentSchemeEvaluation
from app.database.models.scheme import PolicyChangeEvent, PolicyComparison

router = APIRouter()

@router.get("/impacts/me")
async def get_my_impacts(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    result = await db.execute(
        select(StudentImpact).where(
            StudentImpact.student_id == uuid.UUID(current_user.user_id)
        ).order_by(StudentImpact.created_at.desc()).limit(20)
    )
    impacts = result.scalars().all()
    return [
        {
            "id": str(i.id),
            "scheme_id": str(i.scheme_id),
            "old_eligibility": i.old_eligibility,
            "new_eligibility": i.new_eligibility,
            "eligibility_changed": i.eligibility_changed,
            "impact_summary": i.impact_summary,
            "created_at": i.created_at.isoformat(),
        }
        for i in impacts
    ]
