"""
Alembic async migration environment.
Uses SQLAlchemy asyncpg driver for async migrations.
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ---------------------------------------------------------------------------
# Import all models so Alembic can detect them for autogenerate
# ---------------------------------------------------------------------------
from app.database.models.base import Base  # noqa: F401
from app.database.models.user import User  # noqa: F401
from app.database.models.scheme import (  # noqa: F401
    Scheme,
    SchemeSource,
    SchemeVersion,
    SchemeDocument,
    SchemeRule,
    PolicyComparison,
    PolicyChangeEvent,
)
from app.database.models.application import Application  # noqa: F401
from app.database.models.document import Document  # noqa: F401
from app.core.config import settings

# ---------------------------------------------------------------------------
# Alembic Config object (access to alembic.ini values)
# ---------------------------------------------------------------------------
config = context.config

# Inject real DB URL from settings (overrides alembic.ini placeholder)
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url_sync or settings.database_url.replace(
        "postgresql+asyncpg://", "postgresql://"
    ),
)

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# Offline migrations (no DB connection required)
# ---------------------------------------------------------------------------


def run_migrations_offline() -> None:
    """Run migrations using a URL — no DB connection required."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online migrations (async)
# ---------------------------------------------------------------------------


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations using an async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Entry point for online async migrations."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
