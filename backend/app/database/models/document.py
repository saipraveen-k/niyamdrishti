"""
Document upload and processing job models.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database.types import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin, UUIDMixin


class DocumentUpload(Base, UUIDMixin, TimestampMixin):
    """
    Student-uploaded document (not official notifications).
    Kept in private storage with configurable retention.
    """

    __tablename__ = "document_uploads"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    document_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="income_certificate|caste_certificate|marksheet|bonafide|aadhaar_masked|other",
    )
    original_filename: Mapped[str] = mapped_column(String(300), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    sha256_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_document_uploads_user_id", "user_id"),
        Index("ix_document_uploads_expires_at", "expires_at"),
    )


class DocumentProcessingJob(Base, UUIDMixin, TimestampMixin):
    """
    Background processing job for document extraction.
    Acts as a lightweight PostgreSQL-backed job queue.
    """

    __tablename__ = "document_processing_jobs"

    # What document is being processed
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="scheme_document|student_upload",
    )
    job_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="extract_text|ocr|extract_rules|compare_versions",
    )

    # Idempotency
    idempotency_key: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    # Status management
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="queued",
        comment="queued|processing|completed|failed|dead",
    )
    priority: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    # Timing
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_retry_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Retry tracking
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3, nullable=False)

    # Results
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    progress_pct: Mapped[int] = mapped_column(Integer, default=0)

    # Context
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    job_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    attempts: Mapped[list["DocumentProcessingAttempt"]] = relationship(
        back_populates="job", order_by="desc(DocumentProcessingAttempt.started_at)"
    )

    __table_args__ = (
        Index("ix_jobs_status_scheduled", "status", "scheduled_at"),
        Index("ix_jobs_document_id", "document_id"),
    )


class DocumentProcessingAttempt(Base, UUIDMixin, TimestampMixin):
    """Log of each processing attempt for debugging."""

    __tablename__ = "document_processing_attempts"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("document_processing_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    worker_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    job: Mapped["DocumentProcessingJob"] = relationship(back_populates="attempts")
