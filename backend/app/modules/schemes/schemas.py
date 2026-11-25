"""
Pydantic schemas for Scheme endpoints.
"""

from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class SchemeListItem(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    department: Optional[str] = None
    state: str
    scheme_type: str
    education_levels: Optional[list] = None
    eligible_categories: Optional[list] = None
    latest_amount: Optional[Decimal] = None
    latest_deadline: Optional[datetime] = None
    official_url: Optional[str] = None
    is_active: bool
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SchemeDetail(SchemeListItem):
    scheme_identifier: Optional[str] = None
    district: Optional[str] = None
    application_url: Optional[str] = None


class SchemeCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=400)
    description: Optional[str] = None
    department: Optional[str] = None
    scheme_identifier: Optional[str] = None
    state: str
    district: Optional[str] = None
    education_levels: Optional[List[str]] = None
    eligible_categories: Optional[List[str]] = None
    scheme_type: str = "scholarship"
    official_url: Optional[str] = None
    application_url: Optional[str] = None


class SchemeUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=400)
    description: Optional[str] = None
    department: Optional[str] = None
    state: Optional[str] = None
    education_levels: Optional[List[str]] = None
    eligible_categories: Optional[List[str]] = None
    is_published: Optional[bool] = None
    official_url: Optional[str] = None
    application_url: Optional[str] = None


class SchemeSearchParams(BaseModel):
    q: Optional[str] = None
    state: Optional[str] = None
    education_level: Optional[str] = None
    scheme_type: Optional[str] = None
    category: Optional[str] = None
    max_income: Optional[int] = None
    min_marks: Optional[float] = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)


class SchemeListResponse(BaseModel):
    items: List[SchemeListItem]
    total: int
    page: int
    per_page: int
    has_next: bool
