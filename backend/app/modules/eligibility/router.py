"""
Eligibility evaluation endpoints.
"""

import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import AuthUser, get_current_user
from app.database.database import get_db
from app.database.models.application import StudentSchemeEvaluation
from app.database.models.scheme import Scheme, SchemeRule, SchemeVersion
from app.database.models.user import StudentProfile
from app.modules.eligibility.engine import EligibilityResult, eligibility_engine

router = APIRouter()


class EligibilityEvaluateRequest(BaseModel):
    scheme_id: uuid.UUID
    # Optional: override profile fields for simulation
    profile_overrides: Optional[Dict[str, Any]] = None
    is_simulation: bool = False


class CriterionResultOut(BaseModel):
    rule_id: str
    rule_category: str
    rule_key: str
    result: str
    is_mandatory: bool
    student_value: Optional[Any]
    required_condition: dict
    explanation: str
    source_page: Optional[int] = None
    confidence: Optional[float] = None


class EligibilityEvaluateResponse(BaseModel):
    scheme_id: uuid.UUID
    scheme_name: str
    overall_result: str
    match_score: float
    criterion_results: List[CriterionResultOut]
    missing_fields: List[str]
    unknown_rules: List[str]
    passed_mandatory: int
    failed_mandatory: int
    total_mandatory: int
    is_simulation: bool
    evaluation_id: Optional[uuid.UUID] = None
    disclaimer: str = (
        "This eligibility assessment is based on user-provided profile information "
        "and extracted scheme rules. It is NOT an official eligibility determination. "
        "Always verify eligibility with the official scheme authority."
    )


def _build_profile_from_student(sp: StudentProfile) -> Dict[str, Any]:
    """Convert StudentProfile ORM object to flat profile dict for engine."""
    from datetime import datetime, timezone

    profile: Dict[str, Any] = {}

    if sp.caste_category:
        profile["caste_category"] = sp.caste_category
    if sp.is_pwd is not None:
        profile["is_pwd"] = sp.is_pwd
    if sp.education_level:
        profile["education_level"] = sp.education_level
    if sp.course_name:
        profile["course_name"] = sp.course_name
    if sp.marks_percentage is not None:
        profile["marks_percentage"] = sp.marks_percentage
    if sp.cgpa is not None:
        profile["cgpa"] = sp.cgpa
    if sp.annual_family_income is not None:
        profile["annual_family_income"] = sp.annual_family_income
    if sp.state:
        profile["state"] = sp.state
        profile["domicile_state"] = sp.domicile_state or sp.state
    if sp.date_of_birth:
        now = datetime.now(timezone.utc)
        age = (now.date() - sp.date_of_birth.date()).days // 365
        profile["age_years"] = age

    return profile


@router.post("/eligibility/evaluate", response_model=EligibilityEvaluateResponse)
async def evaluate_eligibility(
    request: EligibilityEvaluateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    """
    Evaluate a student's eligibility for a scheme.
    Uses the deterministic Python engine — no AI guessing.
    """
    # Fetch scheme
    scheme_result = await db.execute(
        select(Scheme).where(
            Scheme.id == request.scheme_id,
            Scheme.deleted_at == None,
        )
    )
    scheme = scheme_result.scalar_one_or_none()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    # Fetch active version with approved rules
    version_result = await db.execute(
        select(SchemeVersion).where(
            SchemeVersion.scheme_id == request.scheme_id,
            SchemeVersion.is_approved == True,
            SchemeVersion.is_active == True,
        )
    )
    version = version_result.scalar_one_or_none()
    if not version:
        raise HTTPException(
            status_code=422,
            detail="No approved scheme version available for evaluation",
        )

    # Fetch approved rules
    rules_result = await db.execute(
        select(SchemeRule).where(
            SchemeRule.version_id == version.id,
            SchemeRule.review_status == "approved",
        )
    )
    rules = rules_result.scalars().all()

    if not rules:
        raise HTTPException(
            status_code=422,
            detail="No approved rules available for this scheme version",
        )

    # Build profile dict
    if request.is_simulation and request.profile_overrides:
        # Simulation mode: use provided overrides directly
        profile = request.profile_overrides
    else:
        # Real evaluation: load student profile
        sp_result = await db.execute(
            select(StudentProfile).where(
                StudentProfile.user_id == uuid.UUID(current_user.user_id)
            )
        )
        sp = sp_result.scalar_one_or_none()
        if not sp:
            raise HTTPException(
                status_code=422,
                detail="Student profile not found. Please complete your profile first.",
            )
        profile = _build_profile_from_student(sp)
        if request.profile_overrides:
            profile.update(request.profile_overrides)

    # Build rules list for engine
    rules_list = [
        {
            "id": str(r.id),
            "rule_category": r.rule_category,
            "rule_key": r.rule_key,
            "condition": r.condition,
            "is_mandatory": r.is_mandatory,
            "source_page": r.source_page,
            "confidence": r.confidence,
        }
        for r in rules
    ]

    # Run deterministic evaluation
    report = eligibility_engine.evaluate(rules_list, profile)

    # Persist result (skip for simulations)
    evaluation_id = None
    if not request.is_simulation:
        evaluation = StudentSchemeEvaluation(
            student_id=uuid.UUID(current_user.user_id),
            scheme_id=request.scheme_id,
            version_id=version.id,
            overall_result=report.overall_result.value,
            match_score=report.match_score,
            criterion_results=[
                {
                    "rule_id": r.rule_id,
                    "result": r.result.value,
                    "explanation": r.explanation,
                }
                for r in report.criterion_results
            ],
            unknown_rules=report.unknown_rules,
            missing_fields=report.missing_fields,
        )
        db.add(evaluation)
        await db.flush()
        evaluation_id = evaluation.id

    criterion_out = [
        CriterionResultOut(
            rule_id=r.rule_id,
            rule_category=r.rule_category,
            rule_key=r.rule_key,
            result=r.result.value,
            is_mandatory=r.is_mandatory,
            student_value=r.student_value,
            required_condition=r.required_condition,
            explanation=r.explanation,
            source_page=r.source_page,
            confidence=r.confidence,
        )
        for r in report.criterion_results
    ]

    return EligibilityEvaluateResponse(
        scheme_id=request.scheme_id,
        scheme_name=scheme.name,
        overall_result=report.overall_result.value,
        match_score=report.match_score,
        criterion_results=criterion_out,
        missing_fields=report.missing_fields,
        unknown_rules=report.unknown_rules,
        passed_mandatory=report.passed_mandatory,
        failed_mandatory=report.failed_mandatory,
        total_mandatory=report.total_mandatory,
        is_simulation=request.is_simulation,
        evaluation_id=evaluation_id,
    )
