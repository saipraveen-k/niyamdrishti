# Deployment Guide

## Overview

| Service | Platform | Region |
|---|---|---|
| Frontend | Vercel | Singapore (sin1) |
| Backend API | Render | Singapore |
| Database | Supabase (PostgreSQL) | ap-southeast-1 |
| Auth + Storage | Supabase | ap-southeast-1 |

---

## 1. Supabase setup

1. Create a new project at [supabase.com](https://supabase.com). Choose the **Singapore** region.
2. Note your **Project URL**, **anon key**, and **service role key** from Project Settings → API.
3. Under **Database → Connection string**, copy the **URI** (use the `postgresql://` format for sync and add `+asyncpg` for async).
4. Create storage buckets:
   - `official-documents` — private
   - `student-uploads` — private
   - `generated-reports` — private

No manual SQL migrations are needed — the FastAPI Alembic migration will create all tables.

---

## 2. Backend on Render

### Option A: render.yaml (recommended)

The repository includes `backend/render.yaml` for infrastructure-as-code deployment.

1. Connect your GitHub repository in the Render dashboard.
2. Render will detect `render.yaml` and provision the web service and PostgreSQL database automatically.
3. After provisioning, set the following **secret** environment variables in Render → Environment:

   | Variable | Value |
   |---|---|
   | `SUPABASE_URL` | Your Supabase project URL |
   | `SUPABASE_ANON_KEY` | Supabase anon key |
   | `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key |
   | `OPENAI_API_KEY` | Your OpenAI key (or leave blank) |
   | `ANTHROPIC_API_KEY` | Your Anthropic key (or leave blank) |
   | `FRONTEND_URL` | Your Vercel deployment URL |
   | `ALLOWED_ORIGINS` | Same as `FRONTEND_URL` |

4. Run the initial migration:
   ```bash
   # From Render Shell or locally pointing at the production DB:
   cd backend
   alembic upgrade head
   python -m scripts.seed_schemes
   ```

### Option B: Manual Docker deployment

```bash
docker build -t niyamdrishti-api ./backend
docker run -d \
  -p 8000:8000 \
  --env-file backend/.env \
  niyamdrishti-api
```

---

## 3. Frontend on Vercel

1. Import the repository in the [Vercel dashboard](https://vercel.com).
2. Set **Root Directory** to `frontend`.
3. Add environment variables:

   | Variable | Value |
   |---|---|
   | `NEXT_PUBLIC_API_URL` | Your Render backend URL (e.g. `https://niyamdrishti-api.onrender.com`) |
   | `NEXT_PUBLIC_SUPABASE_URL` | Your Supabase project URL |
   | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key |

4. Deploy. Vercel will auto-detect Next.js and use the `vercel.json` configuration.

**Important:** Update `vercel.json` → `rewrites[0].destination` to match your actual Render URL before deploying to production.

---

## 4. Running database migrations

### From local machine targeting production DB

```bash
export DATABASE_URL_SYNC=postgresql://user:pass@db.supabase.co:5432/postgres
cd backend
source venv/bin/activate
alembic upgrade head
```

### Generate a new migration after model changes

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

### Roll back one migration

```bash
alembic downgrade -1
```

---

## 5. CI/CD

GitHub Actions is configured in `.github/workflows/ci.yml`:

- **On every push/PR:** backend pytest + frontend TypeScript check + Next.js build
- **On main only:** `pip-audit` security scan

For automatic Render deploy on merge to main, enable **Auto Deploy** in the Render service settings and connect to your GitHub repository.

---

## 6. Post-deployment checklist

- [ ] `GET /health` returns `{"status": "ok"}`
- [ ] Supabase Auth: test sign-up and sign-in via the frontend
- [ ] Admin user: set role to `admin` in Supabase's `users` table or via the users API
- [ ] Upload a sample scheme PDF via `/api/v1/documents/upload` and verify extraction
- [ ] Verify rule review queue at `/reviewer`
- [ ] Approve rules and confirm eligibility evaluation works at `/eligibility`
- [ ] Test ChangeLens comparison between two approved versions
- [ ] Verify AI Assistant returns citations (requires approved rules + AI API key)

---

## 7. Scaling notes

- **Render Starter** (free tier) spins down after 15 minutes of inactivity. Upgrade to **Starter Plus** or **Standard** for always-on deployments.
- **Worker processes:** Increase `UVICORN_WORKERS` env var (default: 2) for higher throughput. Each worker uses a separate DB connection pool.
- **Database connection pooling:** For > 10 concurrent users, consider enabling Supabase's PgBouncer connection pooler.
- **Document processing:** Heavy OCR workloads should be moved to a separate Render background worker to avoid blocking the web service.
