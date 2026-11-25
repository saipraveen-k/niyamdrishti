# Local Setup

## Short Explanation

Follow this step-by-step guide to run both the FastAPI backend and Next.js frontend locally without Docker, on either **Windows (PowerShell)** or **macOS/Linux (Bash)**.

---

## 1. Environment Files

1. Copy `backend/.env.example` → `backend/.env` and fill in `SECRET_KEY` (at least 32 characters), `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL`, and optionally `OPENAI_API_KEY`.
2. Copy `frontend/.env.example` → `frontend/.env.local` and fill in `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, and `NEXT_PUBLIC_API_URL=http://localhost:8000`.

See [Environment Variables](ENVIRONMENT_VARIABLES.md) for every variable.

---

## 2. Backend Setup & Startup

### Windows (PowerShell)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m scripts.seed_schemes
uvicorn app.main:app --reload
```

### macOS / Linux (Bash)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m scripts.seed_schemes
uvicorn app.main:app --reload
```

> [!WARNING]
> Do not run `alembic upgrade head` until the missing initial migration is generated and `backend/app/database/migrations/env.py` model imports are fixed. See [Database Setup](DATABASE_SETUP.md) and [Database Migrations](../05-database-and-api/DATABASE_MIGRATIONS.md).

---

## 3. Frontend Setup & Startup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

---

## Related Documentation

- [Backend Setup](BACKEND_SETUP.md)
- [Frontend Setup](FRONTEND_SETUP.md)
- [Database Setup](DATABASE_SETUP.md)
- [Docker Setup](DOCKER_SETUP.md)

