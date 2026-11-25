import hashlib
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import AuthUser, get_current_user, require_roles
from app.database.database import get_db
from app.database.models.document import DocumentProcessingJob
from app.database.models.scheme import SchemeDocument
from app.modules.documents.service import validate_upload, extract_text, compute_sha256
from datetime import datetime, timezone
import os

router = APIRouter()

@router.post("/documents/upload", status_code=201)
async def upload_official_document(
    scheme_id: uuid.UUID = Form(...),
    source_url: str = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(require_roles("admin", "super_admin")),
):
    data = await file.read()
    is_valid, reason = validate_upload(data, file.filename or "", file.content_type or "")
    if not is_valid:
        raise HTTPException(status_code=422, detail=reason)
    
    sha256 = compute_sha256(data)
    storage_path = f"official-documents/{scheme_id}/{sha256[:8]}-{file.filename}"
    
    doc = SchemeDocument(
        scheme_id=scheme_id,
        uploaded_by=uuid.UUID(current_user.user_id),
        original_filename=file.filename or "document",
        storage_path=storage_path,
        file_size_bytes=len(data),
        mime_type=file.content_type or "application/octet-stream",
        sha256_hash=sha256,
        source_url=source_url,
    )
    db.add(doc)
    await db.flush()

    # Queue processing job
    job = DocumentProcessingJob(
        document_id=doc.id,
        document_type="scheme_document",
        job_type="extract_rules",
        idempotency_key=f"extract_{sha256}",
        status="queued",
        priority=5,
        scheduled_at=datetime.now(timezone.utc),
        created_by=uuid.UUID(current_user.user_id),
    )
    db.add(job)
    await db.flush()

    return {
        "document_id": str(doc.id),
        "job_id": str(job.id),
        "status": "queued",
        "message": "Document uploaded. Processing queued.",
    }

@router.get("/documents/{document_id}/status")
async def get_document_status(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    from sqlalchemy import select
    result = await db.execute(
        select(DocumentProcessingJob).where(DocumentProcessingJob.document_id == document_id)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Processing job not found")
    return {
        "document_id": str(document_id),
        "status": job.status,
        "progress_pct": job.progress_pct,
        "attempt_count": job.attempt_count,
        "error_message": job.error_message,
    }
