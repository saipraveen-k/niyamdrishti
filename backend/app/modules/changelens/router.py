"""
ChangeLens API endpoints — policy version comparison.
"""

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import AuthUser, get_current_user, require_roles
from app.database.database import get_db
from app.database.models.scheme import (
    PolicyChangeEvent,
    PolicyComparison,
    SchemeRule,
    SchemeVersion,
)
from app.modules.changelens.comparison_engine import ChangeType, comparison_engine

router = APIRouter()


class CompareVersionsRequest(BaseModel):
    scheme_id: uuid.UUID
    old_version_id: uuid.UUID
    new_version_id: uuid.UUID


class ChangeEventOut(BaseModel):
    id: Optional[uuid.UUID] = None
    change_type: str
    rule_category: str
    rule_key: str
    old_value: Optional[dict] = None
    new_value: Optional[dict] = None
    old_source_text: Optional[str] = None
    new_source_text: Optional[str] = None
    old_source_page: Optional[int] = None
    new_source_page: Optional[int] = None
    significance: str
    human_summary: str


class PolicyComparisonResponse(BaseModel):
    comparison_id: uuid.UUID
    scheme_id: uuid.UUID
    old_version_id: uuid.UUID
    new_version_id: uuid.UUID
    total_changes: int
    high_severity: int
    medium_severity: int
    low_severity: int
    changes: List[ChangeEventOut]


@router.post(
    "/policy-comparisons",
    response_model=PolicyComparisonResponse,
    dependencies=[Depends(require_roles("admin", "super_admin", "document_reviewer"))],
)
async def create_policy_comparison(
    request: CompareVersionsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    """
    Compare two approved scheme versions and produce a change report.
    Only approved rules are compared.
    """
    # Validate versions exist and belong to the scheme
    for version_id in [request.old_version_id, request.new_version_id]:
        v = await db.execute(
            select(SchemeVersion).where(
                SchemeVersion.id == version_id,
                SchemeVersion.scheme_id == request.scheme_id,
            )
        )
        if not v.scalar_one_or_none():
            raise HTTPException(
                status_code=404,
                detail=f"Version {version_id} not found for this scheme",
            )

    # Fetch approved rules for each version
    async def _get_rules(version_id: uuid.UUID) -> List[dict]:
        result = await db.execute(
            select(SchemeRule).where(
                SchemeRule.version_id == version_id,
                SchemeRule.review_status == "approved",
            )
        )
        return [
            {
                "id": str(r.id),
                "rule_category": r.rule_category,
                "rule_key": r.rule_key,
                "condition": r.condition,
                "source_text": r.source_text,
                "source_page": r.source_page,
                "is_mandatory": r.is_mandatory,
                "confidence": r.confidence,
            }
            for r in result.scalars().all()
        ]

    old_rules = await _get_rules(request.old_version_id)
    new_rules = await _get_rules(request.new_version_id)

    if not old_rules and not new_rules:
        raise HTTPException(
            status_code=422,
            detail="No approved rules in either version",
        )

    # Run deterministic comparison
    changes = comparison_engine.compare(old_rules, new_rules)

    # Persist comparison record
    comparison = PolicyComparison(
        scheme_id=request.scheme_id,
        old_version_id=request.old_version_id,
        new_version_id=request.new_version_id,
        created_by=uuid.UUID(current_user.user_id),
        summary={
            "total_changes": len(changes),
            "high": sum(1 for c in changes if c.severity.value == "high"),
            "medium": sum(1 for c in changes if c.severity.value == "medium"),
            "low": sum(1 for c in changes if c.severity.value == "low"),
        },
    )
    db.add(comparison)
    await db.flush()

    # Persist change events
    change_event_records = []
    for change in changes:
        event = PolicyChangeEvent(
            comparison_id=comparison.id,
            change_type=change.change_type.value,
            rule_category=change.rule_category,
            rule_key=change.rule_key,
            old_value=change.old_condition,
            new_value=change.new_condition,
            old_source_text=change.old_source_text,
            new_source_text=change.new_source_text,
            old_source_page=change.old_source_page,
            new_source_page=change.new_source_page,
            significance=change.severity.value,
        )
        db.add(event)
        change_event_records.append(event)

    await db.flush()

    changes_out = [
        ChangeEventOut(
            id=ce.id,
            change_type=c.change_type.value,
            rule_category=c.rule_category,
            rule_key=c.rule_key,
            old_value=c.old_condition,
            new_value=c.new_condition,
            old_source_text=c.old_source_text,
            new_source_text=c.new_source_text,
            old_source_page=c.old_source_page,
            new_source_page=c.new_source_page,
            significance=c.severity.value,
            human_summary=c.human_summary,
        )
        for c, ce in zip(changes, change_event_records)
    ]

    return PolicyComparisonResponse(
        comparison_id=comparison.id,
        scheme_id=request.scheme_id,
        old_version_id=request.old_version_id,
        new_version_id=request.new_version_id,
        total_changes=len(changes),
        high_severity=sum(1 for c in changes_out if c.significance == "high"),
        medium_severity=sum(1 for c in changes_out if c.significance == "medium"),
        low_severity=sum(1 for c in changes_out if c.significance == "low"),
        changes=changes_out,
    )


@router.get(
    "/policy-comparisons/{comparison_id}",
    response_model=PolicyComparisonResponse,
)
async def get_policy_comparison(
    comparison_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    result = await db.execute(
        select(PolicyComparison).where(PolicyComparison.id == comparison_id)
    )
    comparison = result.scalar_one_or_none()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")

    events_result = await db.execute(
        select(PolicyChangeEvent).where(
            PolicyChangeEvent.comparison_id == comparison_id
        )
    )
    events = events_result.scalars().all()

    changes_out = [
        ChangeEventOut(
            id=e.id,
            change_type=e.change_type,
            rule_category=e.rule_category,
            rule_key=e.rule_key,
            old_value=e.old_value,
            new_value=e.new_value,
            old_source_text=e.old_source_text,
            new_source_text=e.new_source_text,
            old_source_page=e.old_source_page,
            new_source_page=e.new_source_page,
            significance=e.significance,
            human_summary=comparison_engine._summary_modified(
                e.rule_category, e.rule_key,
                {"condition": e.old_value},
                {"condition": e.new_value},
            ) if e.change_type == "modified" else f"{e.change_type}: {e.rule_key}",
        )
        for e in events
    ]

    summary = comparison.summary or {}
    return PolicyComparisonResponse(
        comparison_id=comparison.id,
        scheme_id=comparison.scheme_id,
        old_version_id=comparison.old_version_id,
        new_version_id=comparison.new_version_id,
        total_changes=summary.get("total_changes", len(events)),
        high_severity=summary.get("high", 0),
        medium_severity=summary.get("medium", 0),
        low_severity=summary.get("low", 0),
        changes=changes_out,
    )
