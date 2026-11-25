# NiyamDrishti

AI-powered government policy intelligence and student scholarship platform for Andhra Pradesh, Telangana, and India.

---

## What it does

NiyamDrishti helps students discover scholarships and government benefit schemes, understand eligibility without guesswork, track policy changes across document versions, and take personalised action — all in one place.

**Key features**

| Feature | Description |
|---|---|
| Scheme Discovery | Search and filter government schemes by state, category, education level |
| Eligibility Check | Deterministic rule evaluation against your profile — no AI guessing |
| ChangeLens | Side-by-side policy version comparison with structured diff |
| LifeMap | Personalised action plans with milestone tracking |
| AI Assistant | RAG-powered Q&A over official scheme documents with citations |
| Reviewer Workflow | Human review queue for AI-extracted eligibility rules |
| Admin Dashboard | Scheme management, document uploads, processing jobs |

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS v4 |
| Backend | FastAPI, Python 3.11, SQLAlchemy 2.0 async |
| Database | PostgreSQL 16 (Supabase) |
| Auth | Supabase Auth (JWT) |
| Storage | Supabase Storage |
| AI | OpenAI GPT-4o / Anthropic Claude 3.5 (configurable) |
| Deployment | Vercel (frontend), Render (backend) |

---

## Project structure

```
NiyamDrishti/
├── frontend/               # Next.js 16 App Router
│   ├── src/
│   │   ├── app/            # Pages (App Router)
│   │   ├── components/     # UI + feature components
│   │   ├── hooks/          # React query hooks
│   │   ├── lib/            # API client, Supabase
│   │   └── types/          # Shared TypeScript types
│   └── vercel.json
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── core/           # Config, security, logging
│   │   ├── database/       # Models, migrations, session
│   │   ├── modules/        # Feature routers + services
│   │   │   ├── eligibility/engine.py    # Deterministic evaluation
│   │   │   ├── changelens/comparison_engine.py
│   │   │   └── ...
│   │   ├── ai/             # AI provider abstraction
│   │   └── workers/        # Background job processing
│   ├── tests/              # pytest suite
│   ├── scripts/            # seed_schemes.py, etc.
│   ├── Dockerfile
│   └── render.yaml
├── docs/                   # Architecture, deployment, known limitations
├── scripts/                # setup.sh
└── docker-compose.yml
```

---

## Quick start

### Prerequisites

- Python 3.11+
- Node.js 20+
- A Supabase project (free tier works)
- OpenAI or Anthropic API key (optional — AI features disabled without it)

### 1. Clone and configure

```bash
git clone https://github.com/saipraveen-k/niyamdrishti.git
cd niyamdrishti
bash scripts/setup.sh
```

### 2. Configure environment

**Backend** (`backend/.env`):
```env
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-at-least-32-chars

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/niyamdrishti
DATABASE_URL_SYNC=postgresql://user:pass@localhost:5432/niyamdrishti

OPENAI_API_KEY=sk-...          # or leave blank to disable AI
AI_PROVIDER=openai
FRONTEND_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 3. Run migrations and seed data

```bash
cd backend
source venv/bin/activate
alembic upgrade head
python -m scripts.seed_schemes
```

### 4. Start development servers

```bash
# Terminal 1 — Backend
cd backend && source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd frontend
npm run dev
```

Or with Docker:

```bash
docker compose up
```

Open [http://localhost:3000](http://localhost:3000).

---

## Running tests

```bash
cd backend
source venv/bin/activate
pytest -v
```

---

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for Render + Vercel deployment instructions.

---

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for a detailed system diagram and design decisions.

---

## Known limitations

See [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md).

---

## Disclaimer

NiyamDrishti is an independent informational tool. It is **not** affiliated with any government body. Eligibility decisions shown are automated assessments based on extracted document rules — they do **not** constitute official determinations. Always verify with the scheme's official issuing authority before applying.
