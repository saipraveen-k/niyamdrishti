import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import AuthUser, get_current_user
from app.database.database import get_db
from app.database.models.application import ActionPlan, ActionTask

router = APIRouter()

class CreateActionPlanRequest(BaseModel):
    scheme_id: uuid.UUID
    evaluation_id: Optional[uuid.UUID] = None

@router.get("/action-plans/me")
async def get_my_action_plans(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    result = await db.execute(
        select(ActionPlan).where(
            ActionPlan.student_id == uuid.UUID(current_user.user_id),
            ActionPlan.status == "active",
        )
    )
    plans = result.scalars().all()
    return [{"id": str(p.id), "scheme_id": str(p.scheme_id), "status": p.status} for p in plans]

@router.post("/action-plans", status_code=201)
async def create_action_plan(
    data: CreateActionPlanRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    plan = ActionPlan(
        student_id=uuid.UUID(current_user.user_id),
        scheme_id=data.scheme_id,
        evaluation_id=data.evaluation_id,
    )
    db.add(plan)
    await db.flush()
    
    # Create default tasks
    default_tasks = [
        ("document", "Gather required documents", 1),
        ("application_step", "Complete online application form", 2),
        ("verification", "Submit application before deadline", 3),
    ]
    for task_type, title, order in default_tasks:
        db.add(ActionTask(plan_id=plan.id, task_type=task_type, title=title, order_index=order))
    await db.flush()
    return {"plan_id": str(plan.id), "status": "created"}
