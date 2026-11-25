"""
Scheme API endpoints.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import AuthUser, get_current_user, get_optional_user, require_roles
from app.database.database import get_db
from app.modules.schemes.schemas import (
    SchemeCreateRequest,
    SchemeDetail,
    SchemeListResponse,
    SchemeUpdateRequest,
    SchemeSearchParams,
)
from app.modules.schemes.service import SchemeService

router = APIRouter()


@router.get("/schemes", response_model=SchemeListResponse)
async def list_schemes(
    q: Optional[str] = Query(None, description="Search query"),
    state: Optional[str] = Query(None),
    education_level: Optional[str] = Query(None),
    scheme_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    max_income: Optional[int] = Query(None),
    min_marks: Optional[float] = Query(None),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user: Optional[AuthUser] = Depends(get_optional_user),
):
    """Public scheme discovery. No authentication required."""
    params = SchemeSearchParams(
        q=q,
        state=state,
        education_level=education_level,
        scheme_type=scheme_type,
        category=category,
        max_income=max_income,
        min_marks=min_marks,
        page=page,
        per_page=per_page,
    )
    service = SchemeService(db)
    return await service.list_schemes(params)


@router.get("/schemes/{scheme_id}", response_model=SchemeDetail)
async def get_scheme(
    scheme_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user: Optional[AuthUser] = Depends(get_optional_user),
):
    """Get scheme details. Public endpoint."""
    service = SchemeService(db)
    scheme = await service.get_scheme(scheme_id)
    if not scheme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    if not scheme.is_published:
        # Only admins can view unpublished schemes
        if not _user or _user.app_role not in ("admin", "super_admin"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    return scheme


@router.post(
    "/admin/schemes",
    response_model=SchemeDetail,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
async def create_scheme(
    data: SchemeCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    """Admin: create a new scheme."""
    service = SchemeService(db)
    return await service.create_scheme(data)


@router.patch(
    "/admin/schemes/{scheme_id}",
    response_model=SchemeDetail,
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
async def update_scheme(
    scheme_id: uuid.UUID,
    data: SchemeUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    service = SchemeService(db)
    scheme = await service.update_scheme(scheme_id, data)
    if not scheme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    return scheme


@router.post(
    "/admin/schemes/{scheme_id}/publish",
    response_model=SchemeDetail,
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
async def publish_scheme(
    scheme_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    service = SchemeService(db)
    scheme = await service.publish_scheme(scheme_id)
    if not scheme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    return scheme


@router.post("/schemes/{scheme_id}/bookmark", status_code=status.HTTP_204_NO_CONTENT)
async def bookmark_scheme(
    scheme_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    """Student: save/bookmark a scheme."""
    from app.database.models.application import SavedScheme
    from sqlalchemy import select, delete

    # Toggle bookmark
    existing = await db.execute(
        select(SavedScheme).where(
            SavedScheme.student_id == uuid.UUID(current_user.user_id),
            SavedScheme.scheme_id == scheme_id,
        )
    )
    saved = existing.scalar_one_or_none()
    if saved:
        await db.execute(
            delete(SavedScheme).where(SavedScheme.id == saved.id)
        )
    else:
        db.add(SavedScheme(
            student_id=uuid.UUID(current_user.user_id),
            scheme_id=scheme_id,
        ))
    await db.flush()
