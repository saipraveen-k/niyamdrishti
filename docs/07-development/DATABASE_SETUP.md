# Database Setup

## Short Explanation

NiyamDrishti uses PostgreSQL 16 (hosted on Supabase in production, or `postgres:16-alpine` locally via Docker) with SQLAlchemy 2.0 async models and a seed script for 4 representative schemes.

---

## 1. Option A: Supabase Cloud PostgreSQL

1. Create a Supabase project (Singapore `ap-southeast-1` recommended in `docs/DEPLOYMENT.md`).
2. Copy the PostgreSQL connection string into `backend/.env`:
   - `DATABASE_URL=postgresql+asyncpg://postgres:<password>@db.<project>.supabase.co:5432/postgres`
   - `DATABASE_URL_SYNC=postgresql://postgres:<password>@db.<project>.supabase.co:5432/postgres`
3. Create three private storage buckets in Supabase Storage: `official-documents`, `student-uploads`, and `generated-reports`.

## 2. Option B: Local Docker PostgreSQL

Start `postgres` via `docker compose up -d postgres` using the defaults in `docker-compose.yml`:
- DB: `niyamdrishti`, User: `niyamdrishti`, Password: `devpassword`, Port: `5432`.

---

## 3. Creating Tables & Seeding Data

> [!IMPORTANT]
> `backend/app/database/migrations/versions/` currently has no Alembic migration files, and `migrations/env.py` has stale imports (`User`, `Application`, `Document`).
> - Before running `alembic upgrade head`, update `env.py` to import from `app.database.models` and run `alembic revision --autogenerate -m "initial schema"`.
> - Alternatively, for quick local development, tables can be initialized via `Base.metadata.create_all` against your dev database before seeding.

Run the scheme seed script (`backend/scripts/seed_schemes.py`):

```bash
cd backend
python -m scripts.seed_schemes
```

This seeds **4 published schemes** with approved v1 rules:
1. *Post Matric Scholarship for SC Students — Andhra Pradesh* (`₹15,000`)
2. *Dr. YSR Vidyadeeepika Scholarship — Telangana* (`₹20,000`)
3. *National Merit Scholarship — Central Government* (`₹12,000`)
4. *Prime Minister's Research Fellowship* (`₹70,000`)

---

## Related Documentation

- [Database Schema](../05-database-and-api/DATABASE_SCHEMA.md)
- [Database Migrations](../05-database-and-api/DATABASE_MIGRATIONS.md)

