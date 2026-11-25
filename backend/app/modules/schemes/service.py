"""
Scheme business logic.
"""

import re
import uuid
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.database.models.scheme import Scheme
from app.modules.schemes.schemas import (
    SchemeCreateRequest,
    SchemeListResponse,
    SchemeUpdateRequest,
    SchemeSearchParams,
)

logger = get_logger(__name__)


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


class SchemeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_schemes(self, params: SchemeSearchParams) -> SchemeListResponse:
        query = select(Scheme).where(Scheme.is_published == True, Scheme.deleted_at == None)

        if params.q:
            search = f"%{params.q}%"
            query = query.where(
                or_(Scheme.name.ilike(search), Scheme.description.ilike(search))
            )
        if params.state:
            query = query.where(Scheme.state == params.state)
        if params.scheme_type:
            query = query.where(Scheme.scheme_type == params.scheme_type)
        if params.education_level:
            # JSONB contains check
            query = query.where(
                Scheme.education_levels.contains([params.education_level])
            )
        if params.category:
            query = query.where(
                Scheme.eligible_categories.contains([params.category])
            )

        # Count total
        count_q = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_q)
        total = total_result.scalar_one()

        # Paginate
        offset = (params.page - 1) * params.per_page
        query = query.order_by(Scheme.name).offset(offset).limit(params.per_page)

        result = await self.db.execute(query)
        items = result.scalars().all()

        return SchemeListResponse(
            items=list(items),
            total=total,
            page=params.page,
            per_page=params.per_page,
            has_next=(offset + len(items)) < total,
        )

    async def get_scheme(self, scheme_id: uuid.UUID) -> Optional[Scheme]:
        result = await self.db.execute(
            select(Scheme).where(Scheme.id == scheme_id, Scheme.deleted_at == None)
        )
        return result.scalar_one_or_none()

    async def get_scheme_by_slug(self, slug: str) -> Optional[Scheme]:
        result = await self.db.execute(
            select(Scheme).where(Scheme.slug == slug, Scheme.deleted_at == None)
        )
        return result.scalar_one_or_none()

    async def create_scheme(self, data: SchemeCreateRequest) -> Scheme:
        slug = _slugify(data.name)
        # Ensure uniqueness
        existing = await self.get_scheme_by_slug(slug)
        if existing:
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"

        scheme = Scheme(
            name=data.name,
            slug=slug,
            description=data.description,
            department=data.department,
            scheme_identifier=data.scheme_identifier,
            state=data.state,
            district=data.district,
            education_levels=data.education_levels or [],
            eligible_categories=data.eligible_categories or [],
            scheme_type=data.scheme_type,
            official_url=data.official_url,
            application_url=data.application_url,
            is_published=False,
        )
        self.db.add(scheme)
        await self.db.flush()
        logger.info("scheme_created", scheme_id=str(scheme.id), name=scheme.name)
        return scheme

    async def update_scheme(
        self, scheme_id: uuid.UUID, data: SchemeUpdateRequest
    ) -> Optional[Scheme]:
        scheme = await self.get_scheme(scheme_id)
        if not scheme:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(scheme, field, value)

        await self.db.flush()
        logger.info("scheme_updated", scheme_id=str(scheme_id))
        return scheme

    async def publish_scheme(self, scheme_id: uuid.UUID) -> Optional[Scheme]:
        scheme = await self.get_scheme(scheme_id)
        if not scheme:
            return None
        scheme.is_published = True
        await self.db.flush()
        return scheme

    async def soft_delete_scheme(self, scheme_id: uuid.UUID) -> bool:
        from datetime import datetime, timezone
        scheme = await self.get_scheme(scheme_id)
        if not scheme:
            return False
        scheme.deleted_at = datetime.now(timezone.utc)
        await self.db.flush()
        logger.info("scheme_deleted", scheme_id=str(scheme_id))
        return True
