"""
Scheme, scheme versions, scheme rules, and policy comparison models.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID

from app.database.types import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Scheme(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Master scheme record."""

    __tablename__ = "schemes"

    name: Mapped[str] = mapped_column(String(400), nullable=False)
    slug: Mapped[str] = mapped_column(String(400), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    scheme_identifier: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Geographic scope
    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Andhra Pradesh|Telangana|Central|All India",
    )
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Category
    education_levels: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    # e.g. ["ug", "pg"]
    eligible_categories: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    # e.g. ["SC", "ST", "OBC"]
    scheme_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="scholarship",
        comment="scholarship|fellowship|stipend|benefit",
    )

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    # Official URLs
    official_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    application_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Latest version summary (denormalized for fast listing)
    latest_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    latest_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    latest_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    # Relationships
    versions: Mapped[list["SchemeVersion"]] = relationship(
        back_populates="scheme", order_by="desc(SchemeVersion.created_at)"
    )
    documents: Mapped[list["SchemeDocument"]] = relationship(back_populates="scheme")

    __table_args__ = (
        Index("ix_schemes_state", "state"),
        Index("ix_schemes_is_published", "is_published"),
        Index("ix_schemes_scheme_type", "scheme_type"),
    )


class SchemeSource(Base, UUIDMixin, TimestampMixin):
    """Official source for a scheme (notification, circular, etc.)."""

    __tablename__ = "scheme_sources"

    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
    )
    source_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="notification|circular|gazette|website"
    )
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    source_title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)


class SchemeVersion(Base, UUIDMixin, TimestampMixin):
    """
    A versioned snapshot of a scheme's rules.
    Each uploaded document creates a new version after extraction + review.
    """

    __tablename__ = "scheme_versions"

    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    version_label: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    source_document_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheme_documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    extraction_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    scheme: Mapped["Scheme"] = relationship(back_populates="versions")
    rules: Mapped[list["SchemeRule"]] = relationship(back_populates="version")

    __table_args__ = (
        UniqueConstraint("scheme_id", "version_number", name="uq_scheme_version"),
        Index("ix_scheme_versions_scheme_id", "scheme_id"),
    )


class SchemeDocument(Base, UUIDMixin, TimestampMixin):
    """
    Official document uploaded for a scheme.
    Stored privately in Supabase Storage.
    """

    __tablename__ = "scheme_documents"

    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    uploaded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(300), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sha256_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    is_official: Mapped[bool] = mapped_column(Boolean, default=True)

    scheme: Mapped["Scheme"] = relationship(back_populates="documents")

    __table_args__ = (
        Index("ix_scheme_documents_sha256", "sha256_hash"),
    )


class SchemeRule(Base, UUIDMixin, TimestampMixin):
    """
    A single extracted eligibility rule for a scheme version.
    """

    __tablename__ = "scheme_rules"

    version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheme_versions.id", ondelete="CASCADE"),
        nullable=False,
    )
    rule_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="income|marks|age|category|domicile|course|disability|amount|deadline|document|renewal|exclusion|other",
    )
    rule_key: Mapped[str] = mapped_column(String(200), nullable=False)
    # Structured condition as JSONB (operator, value, unit, logic, mandatory)
    condition: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # Raw extracted text from document
    source_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(nullable=True)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    review_status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        comment="pending|approved|rejected",
    )
    reviewed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewer_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    version: Mapped["SchemeVersion"] = relationship(back_populates="rules")

    __table_args__ = (
        Index("ix_scheme_rules_version_id", "version_id"),
        Index("ix_scheme_rules_rule_category", "rule_category"),
    )


class PolicyComparison(Base, UUIDMixin, TimestampMixin):
    """Records a comparison between two scheme versions."""

    __tablename__ = "policy_comparisons"

    scheme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
    )
    old_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheme_versions.id", ondelete="CASCADE"),
        nullable=False,
    )
    new_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheme_versions.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    summary: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    report_storage_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    change_events: Mapped[list["PolicyChangeEvent"]] = relationship(back_populates="comparison")


class PolicyChangeEvent(Base, UUIDMixin, TimestampMixin):
    """A single detected change between two rule versions."""

    __tablename__ = "policy_change_events"

    comparison_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policy_comparisons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    change_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="added|removed|modified",
    )
    rule_category: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_key: Mapped[str] = mapped_column(String(200), nullable=False)
    old_value: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    old_source_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_source_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    old_source_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    new_source_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    significance: Mapped[str] = mapped_column(
        String(20),
        default="medium",
        comment="high|medium|low",
    )

    comparison: Mapped["PolicyComparison"] = relationship(back_populates="change_events")
