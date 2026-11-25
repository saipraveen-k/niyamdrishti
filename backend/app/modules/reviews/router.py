import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import AuthUser, get_current_user, require_roles
from app.database.database import get_db
from app.database.models.scheme import SchemeRule
from datetime import datetime, timezone

router = APIRouter()

class ReviewDecisionRequest(BaseModel):
    decision: str  # approved | rejected
    note: Optional[str] = None
    corrected_condition: Optional[dict] = None

@router.get("/reviews/queue")
async def get_review_queue(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(require_roles("document_reviewer", "admin", "super_admin")),
):
    result = await db.execute(
        select(SchemeRule).where(SchemeRule.review_status == "pending").limit(50)
    )
    rules = result.scalars().all()
    return [
        {
            "id": str(r.id),
            "version_id": str(r.version_id),
            "rule_category": r.rule_category,
            "rule_key": r.rule_key,
            "condition": r.condition,
            "source_text": r.source_text,
            "source_page": r.source_page,
            "confidence": r.confidence,
        }
        for r in rules
    ]

@router.post("/reviews/{rule_id}/approve")
async def approve_rule(
    rule_id: uuid.UUID,
    data: ReviewDecisionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(require_roles("document_reviewer", "admin", "super_admin")),
):
    result = await db.execute(select(SchemeRule).where(SchemeRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    rule.review_status = data.decision
    rule.reviewed_by = uuid.UUID(current_user.user_id)
    rule.reviewed_at = datetime.now(timezone.utc)
    rule.reviewer_note = data.note
    if data.corrected_condition:
        rule.condition = data.corrected_condition
    await db.flush()
    return {"rule_id": str(rule_id), "status": data.decision}
