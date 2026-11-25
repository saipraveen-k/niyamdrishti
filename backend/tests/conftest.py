"""
Pytest configuration and shared fixtures.

Uses an in-memory SQLite database for fast unit tests.
Integration tests that need Postgres should be marked @pytest.mark.integration
and skipped in CI unless INTEGRATION_TESTS=1 is set.
"""

import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# ---------------------------------------------------------------------------
# Environment: point to SQLite for unit tests
# ---------------------------------------------------------------------------

os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("SECRET_KEY", "test-secret-key-must-be-at-least-32-chars-long")
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "test-service-role-key")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("DATABASE_URL_SYNC", "sqlite:///:memory:")

from app.main import app  # noqa: E402  (must come after env setup)
from app.database.database import get_db  # noqa: E402
from app.database.models.base import Base  # noqa: E402

# ---------------------------------------------------------------------------
# In-memory SQLite async engine
# ---------------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def create_tables():
    """Create all tables in the in-memory SQLite DB once per session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)   # clean slate
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(loop_scope="session")
async def db_session():
    """Return a fresh DB session per test, rolled back after each test."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(loop_scope="session")
async def client(db_session: AsyncSession):
    """
    HTTP test client with the DB dependency overridden to use the
    in-memory SQLite session.
    """

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()
