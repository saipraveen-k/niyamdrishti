"""
Custom SQLAlchemy column types.

JSONB: uses PostgreSQL's native JSONB in production; falls back to JSON for
      SQLite (used in unit tests with an in-memory database).
"""

from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB as _PG_JSONB
from sqlalchemy.types import TypeDecorator


class JSONB(TypeDecorator):
    """
    PostgreSQL JSONB in production, plain JSON on other dialects.

    This lets the same model definitions run against both PostgreSQL
    (Render / Supabase) and SQLite (pytest in-memory fixture).
    """

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(_PG_JSONB())
        return dialect.type_descriptor(JSON())
