# Render Deployment

## Short Explanation

The FastAPI backend includes an infrastructure-as-code blueprint (`backend/render.yaml`) for deploying the Python web service and PostgreSQL database on Render in the Singapore region.

---

## 1. Render Blueprint (`backend/render.yaml`)

| Property | Configured Value |
|---|---|
| `type` / `runtime` | `web` / `python` |
| `name` | `niyamdrishti-api` |
| `region` / `plan` | `singapore` / `starter` |
| `rootDir` | `backend` |
| `buildCommand` | `pip install -r requirements.txt` |
| `startCommand` | `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2` |
| `healthCheckPath` | `/health` |
| `autoDeploy` | `true` |
| **Database** | `niyamdrishti-db` (`starter` plan, `databaseName: niyamdrishti`, `user: niyamdrishti`) |

> [!WARNING]
> **Two important notes on `render.yaml`**:
> 1. Render's managed PostgreSQL `connectionString` uses `postgresql://` (or `postgres://`), whereas `backend/app/database/database.py` uses `create_async_engine`, which requires `postgresql+asyncpg://` when pointing at PostgreSQL. If using Supabase PostgreSQL instead of Render DB, set `DATABASE_URL` manually to `postgresql+asyncpg://...`.
> 2. Render's Python native runtime (`pip install -r requirements.txt`) does **not** run `backend/Dockerfile`, so system binaries `tesseract-ocr` and `poppler-utils` are only present if you deploy via Docker runtime instead of native Python runtime.

---

## 2. Secret Environment Variables

Set these `sync: false` variables in the Render dashboard:
`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` (optional), `FRONTEND_URL`, `ALLOWED_ORIGINS`. (`SECRET_KEY` uses `generateValue: true`.)

---

## Related Documentation

- [Deployment Overview](DEPLOYMENT_OVERVIEW.md)
- [Docker Architecture](DOCKER_ARCHITECTURE.md)
- [Database Migrations](../05-database-and-api/DATABASE_MIGRATIONS.md)

