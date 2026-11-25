# Database Migrations

## Short Explanation

NiyamDrishti configures **Alembic `1.14.0`** with an asynchronous SQLAlchemy `asyncpg` migration runner (`backend/app/database/migrations/env.py`) to manage PostgreSQL schema changes.

---

## 1. Current Migration Configuration

- **Config file**: `backend/alembic.ini` (`script_location = app/database/migrations`).
- **Environment script**: `backend/app/database/migrations/env.py` overrides `sqlalchemy.url` using `settings.database_url_sync` or `settings.database_url.replace("postgresql+asyncpg://", "postgresql://")`, and runs online migrations via `asyncio.run(run_async_migrations())` with `pool.NullPool`.
- **Target metadata**: `Base.metadata`.

---

## 2. Current Migration Status & Known Bug (Verified)

> [!CAUTION]
> **Two migration issues exist in the current repository and must be fixed before running `alembic` commands:**
> 1. **No Migration Scripts Yet**: `backend/app/database/migrations/versions/` contains only `.gitkeep` — no initial revision script has been generated yet.
> 2. **Broken Model Imports in `env.py`**: Lines 18, 28, and 29 of `backend/app/database/migrations/env.py` attempt to import `User`, `Application`, and `Document`:
>    ```python
>    from app.database.models.user import User  # does not exist
>    from app.database.models.application import Application  # does not exist
>    from app.database.models.document import Document  # does not exist
>    ```
>    Those class names do not exist in the models (`user.py` defines `UserProfile`, `StudentProfile`, `College`, `CollegeMembership`, `AdminInvitation`; `application.py` defines `StudentSchemeEvaluation`, `SavedScheme`, `StudentImpact`, `ActionPlan`, `ActionTask`, `StudentApplication`, `ApplicationStatusHistory`; `document.py` defines `DocumentUpload`, `DocumentProcessingJob`, `DocumentProcessingAttempt`). `app/database/models/__init__.py` already exports all 22 models cleanly.

---

## 3. Standard Alembic Commands (Once `env.py` Imports Are Fixed)

```bash
cd backend
# Generate initial migration
alembic revision --autogenerate -m "initial schema"

# Apply migrations
alembic upgrade head

# Roll back one revision
alembic downgrade -1
```

*(Note: During unit tests in `tests/conftest.py`, tables are created directly in SQLite in-memory via `Base.metadata.create_all` without Alembic.)*

---

## Related Documentation

- [Database Schema](DATABASE_SCHEMA.md)
- [Database Setup](../07-development/DATABASE_SETUP.md)
- [Known Limitations](../08-testing-and-quality/KNOWN_LIMITATIONS.md)

