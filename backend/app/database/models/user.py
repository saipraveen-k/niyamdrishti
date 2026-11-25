"""
User profile and role models.
user_profiles mirrors Supabase auth.users but stores application-level data.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin, UUIDMixin


class UserProfile(Base, UUIDMixin, TimestampMixin):
    """
    Application-level user profile.
    id == Supabase auth.users.id (UUID).
    Sensitive eligibility data stored here.
    """

    __tablename__ = "user_profiles"

    # Supabase auth user id — this IS the PK and foreign key to auth.users
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        comment="Must match Supabase auth.users.id",
    )

    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    app_role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="student",
        comment="student|college_coordinator|document_reviewer|admin|super_admin",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    student_profile: Mapped[Optional["StudentProfile"]] = relationship(
        back_populates="user", uselist=False, lazy="select"
    )

    __table_args__ = (
        Index("ix_user_profiles_app_role", "app_role"),
    )

    def __repr__(self) -> str:
        return f"<UserProfile {self.email} role={self.app_role}>"


class StudentProfile(Base, UUIDMixin, TimestampMixin):
    """
    Eligibility-relevant student details.
    Linked 1-to-1 with UserProfile.
    """

    __tablename__ = "student_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Demographic
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Category
    # Collect only where relevant to eligibility; must be optional
    caste_category: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="GEN|OBC|SC|ST|EWS — user-declared; not verified",
    )
    is_pwd: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        comment="Person with disability — user-declared",
    )
    pwd_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Education
    education_level: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="10th|12th|ug|pg|phd",
    )
    course_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    college_name: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    college_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("colleges.id", ondelete="SET NULL"),
        nullable=True,
    )
    current_year_semester: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    marks_percentage: Mapped[Optional[float]] = mapped_column(nullable=True)
    cgpa: Mapped[Optional[float]] = mapped_column(nullable=True)

    # Economic
    annual_family_income: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Annual family income in INR — user-declared",
    )

    # Domicile
    domicile_state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    domicile_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Profile completeness (0-100 computed)
    profile_completeness: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    user: Mapped["UserProfile"] = relationship(back_populates="student_profile")

    def __repr__(self) -> str:
        return f"<StudentProfile user_id={self.user_id}>"


class College(Base, UUIDMixin, TimestampMixin):
    """Registered college/university."""

    __tablename__ = "colleges"

    name: Mapped[str] = mapped_column(String(300), nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    affiliation: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        Index("ix_colleges_state", "state"),
    )


class CollegeMembership(Base, UUIDMixin, TimestampMixin):
    """Links a college_coordinator to a college."""

    __tablename__ = "college_memberships"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    college_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("colleges.id", ondelete="CASCADE"),
        nullable=False,
    )
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "college_id", name="uq_college_membership"),
    )


class AdminInvitation(Base, UUIDMixin, TimestampMixin):
    """Invitation for admin/reviewer roles."""

    __tablename__ = "admin_invitations"

    email: Mapped[str] = mapped_column(String(254), nullable=False)
    invited_role: Mapped[str] = mapped_column(String(50), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    invited_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
