# Backup and Recovery

## Short Explanation

Because NiyamDrishti persists all authoritative state—user profiles, scheme versions, approved rules, comparisons, and action plans—in PostgreSQL (Supabase or Render) and uploaded PDFs in Supabase Storage, backup and recovery rely on managed database snapshots, Alembic schema history, and SHA-256 document verification.

---

## 1. Data Durability & Recovery Mechanisms

| Asset | Storage Location | Recovery Strategy | Current Repo Status |
|---|---|---|---|
| **Relational Data (22 tables)** | Supabase PostgreSQL (or Render DB) | Automated daily provider backups / `pg_dump` exports | Managed by Supabase/Render; no custom backup script in repo |
| **Schema Definition** | `backend/app/database/models/` + Alembic | Re-create via Alembic migrations (`alembic upgrade head`) | Models complete; Alembic `versions/` empty (see [Database Migrations](../05-database-and-api/DATABASE_MIGRATIONS.md)) |
| **Representative Seed Data** | `backend/scripts/seed_schemes.py` | Re-run `python -m scripts.seed_schemes` | Implemented (4 schemes) |
| **Official & Student Documents** | Supabase Storage (`official-documents`, `student-uploads`, `generated-reports`) | Private bucket object versioning + `sha256_hash` integrity check | Configured in `config.py`; upload SDK calls not wired yet |
| **Soft-Deleted Schemes** | `schemes.deleted_at` (`SoftDeleteMixin`) | Restore by clearing `deleted_at` | Implemented on `Scheme` model |

---

## 2. Pre-Production Checklist

1. Fix `migrations/env.py` imports and generate the baseline Alembic revision before deploying to production.
2. Enable Point-in-Time Recovery (PITR) or scheduled `pg_dump` backups on your Supabase/Render PostgreSQL plan.
3. Document restore drills and retention compliance (`STUDENT_DOC_RETENTION_DAYS=30`).

---

## Related Documentation

- [Database Migrations](../05-database-and-api/DATABASE_MIGRATIONS.md)
- [Privacy](../04-technical/PRIVACY.md)
- [Deployment Overview](DEPLOYMENT_OVERVIEW.md)

