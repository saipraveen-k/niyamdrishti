"""
Student eligibility, applications, impact, and LifeMap models.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database.types import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin, UUIDMixin


class StudentSchemeEvaluation(Base, UUIDMixin, TimestampMixin):
    """
    Deterministic eligibility evaluation result for a student against a scheme version.
    """

    __tablename__ = "student_scheme_evaluations"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheme_versions.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Overall result
    overall_result: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="eligible|ineligible|unknown|needs_verification",
    )
    match_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    # Criterion-level results as JSONB array
    criterion_results: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # Rules that produced unknown result due to missing profile data
    unknown_rules: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # Missing profile fields needed for complete evaluation
    missing_fields: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    is_latest: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        Index("ix_evaluations_student_scheme", "student_id", "scheme_id"),
    )


class SavedScheme(Base, UUIDMixin, TimestampMixin):
    """Student bookmarked schemes."""

    __tablename__ = "saved_schemes"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
    )

    from sqlalchemy import UniqueConstraint

    __table_args__ = (
        UniqueConstraint("student_id", "scheme_id", name="uq_saved_scheme"),
    )


class StudentImpact(Base, UUIDMixin, TimestampMixin):
    """
    Tracks how a policy change event affects a specific student.
    """

    __tablename__ = "student_impacts"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    comparison_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policy_comparisons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Was student eligible under old version?
    old_eligibility: Mapped[str] = mapped_column(String(20), nullable=False)
    # Is student eligible under new version?
    new_eligibility: Mapped[str] = mapped_column(String(20), nullable=False)
    # Did eligibility change?
    eligibility_changed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    impact_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Detailed per-rule impact
    rule_impacts: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    is_notified: Mapped[bool] = mapped_column(Boolean, default=False)


class ActionPlan(Base, UUIDMixin, TimestampMixin):
    """
    Personalized LifeMap action plan for a student targeting a scheme.
    """

    __tablename__ = "action_plans"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
    )
    evaluation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        comment="active|completed|abandoned",
    )
    report_storage_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    tasks: Mapped[list["ActionTask"]] = relationship(
        back_populates="plan", order_by="ActionTask.order_index"
    )


class ActionTask(Base, UUIDMixin, TimestampMixin):
    """Individual task within an action plan."""

    __tablename__ = "action_tasks"

    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("action_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="document|application_step|deadline|alternative|verification",
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    task_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    plan: Mapped["ActionPlan"] = relationship(back_populates="tasks")


class StudentApplication(Base, UUIDMixin, TimestampMixin):
    """
    Student's manual application status tracker.
    NiyamDrishti does NOT auto-submit to government portals.
    """

    __tablename__ = "student_applications"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="planning",
        comment="planning|documents_gathering|submitted|under_review|approved|rejected|withdrawn",
    )
    applied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    external_application_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    history: Mapped[list["ApplicationStatusHistory"]] = relationship(
        back_populates="application", order_by="desc(ApplicationStatusHistory.created_at)"
    )


class ApplicationStatusHistory(Base, UUIDMixin, TimestampMixin):
    """Audit trail of application status changes."""

    __tablename__ = "application_status_history"

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("student_applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    old_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    new_status: Mapped[str] = mapped_column(String(50), nullable=False)
    changed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    application: Mapped["StudentApplication"] = relationship(back_populates="history")
