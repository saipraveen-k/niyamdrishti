# NiyamDrishti

**Understand policy changes. Discover opportunities. Take the right next step.**

![Next.js](https://img.shields.io/badge/Next.js-16.4.6-black?logo=next.js)
![React](https://img.shields.io/badge/React-19.3.0-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.3.3-06B6D4?logo=tailwindcss)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)
![Supabase](https://img.shields.io/badge/Supabase-Auth%20%26%20DB-3ECF8E?logo=supabase)

---

## Short Description

**NiyamDrishti** (*"Rule Vision"*) is an AI-powered government policy intelligence and personalized student opportunity platform built for students across **Andhra Pradesh, Telangana, and All-India / Central schemes**. It helps learners discover scholarships, evaluate eligibility deterministically without AI guesswork, inspect rule changes across official notification versions (**ChangeLens**), and organize applications through structured checklists (**LifeMap**).

> [!IMPORTANT]
> NiyamDrishti is an independent informational platform and is **not** affiliated with any government authority. It does **not** auto-submit applications or issue official eligibility decisions. Always confirm criteria on official government portals.

---

## Problem Statement

Students in India frequently lose scholarship opportunities because official rules live inside dense, multi-page PDFs and Government Orders (GOs) that change every academic cycle:

1. **Fragmented Portals**: Criteria are scattered across state and central sites.
2. **Silent Policy Amendments**: Income limits, marks cutoffs, and deadlines shift across versions without clear changelogs.
3. **LLM Hallucination Risk**: Generic AI chatbots cannot be trusted to perform strict arithmetic or guarantee pass/fail scholarship eligibility.

---

## Our Solution

NiyamDrishti separates **AI document structuring** from **deterministic Python decision logic** with a mandatory **human-in-the-loop** review gate:

1. **AI Extracts (`OpenAIProvider`)**: Official notifications are validated, parsed via `PyMuPDF` / `Tesseract OCR` / `python-docx`, and structured into Pydantic-validated JSONB conditions anchored to verbatim `source_text` and `source_page`.
2. **Humans Verify (`/reviewer`)**: Every extracted rule enters as `"pending"` and only goes live after explicit approval by a `document_reviewer`, `admin`, or `super_admin`.
3. **Pure Python Evaluates (`EligibilityEngine`)**: Evaluates student profiles deterministically (`passed`, `failed`, or `unknown` with missing-field hints)—never AI guessing.
4. **ChangeLens Compares (`PolicyComparisonEngine`)**: Diffs two approved `SchemeVersion` snapshots into `added`, `removed`, and `modified` events classified by severity (`high`, `medium`, `low`).

---

## Key Innovations

- **AI Extracts, Python Decides**: Zero LLM calls during eligibility checks or policy diffing.
- **Explicit `UNKNOWN` Semantics**: Missing student fields report `unknown` and populate `missing_fields` instead of falsely marking a student ineligible.
- **Page-Level Evidence Anchoring**: Rules and ChangeLens diffs retain `source_text`, `source_page`, and `confidence`.
- **Prompt-Injection Defense**: Document extraction wraps text in `<document>` tags with explicit system-prompt isolation.
- **Cross-Dialect `JSONB` Type**: Runs natively on PostgreSQL `JSONB` in production and `JSON` on SQLite in-memory during CI tests.

---

## Feature Overview

| Feature | Description | Status in Current Repo |
|---|---|---|
| **Scheme Discovery** | Search and filter schemes by state, education level, category, and type | **Implemented** (`max_income`/`min_marks` query filters unused in service) |
| **Eligibility Engine** | Deterministic criterion-by-criterion evaluation + simulation mode | **Implemented** (13/15 unit tests pass; 2 compound-rule tests fail; UI contract needs sync) |
| **ChangeLens** | Deterministic version comparison with severity & source evidence | **Implemented** (14/14 engine tests pass; UI route needs alignment) |
| **Human Reviewer Queue** | Approve/reject AI-extracted rules with confidence badges | **Implemented** |
| **Document Upload & OCR** | Magic-byte validation, SHA-256, PyMuPDF + Tesseract + python-docx | **Partially Implemented** (worker loop & Storage upload not wired yet) |
| **LifeMap & Applications** | Action plans, default tasks, and manual status history tracker | **Partially Implemented** (UI paths & task patching need alignment) |
| **Personalized Impact Engine** | Per-student old vs. new eligibility tracking (`StudentImpact`) | **Partially Implemented** (`GET /impacts/me` exists; computation service planned) |
| **AI Assistant** | Multilingual chat (`en` / `te` / `hi`) with grounding prompt | **Partially Implemented** (direct OpenAI chat; RAG citations & payload sync planned) |
| **Notifications & Admin Jobs** | Alerts and background job monitoring | **Stubbed** (return empty lists) |

See [docs/PROJECT_AUDIT.md](docs/PROJECT_AUDIT.md) for the complete module-by-module audit.

---

## Architecture Diagram

```mermaid
flowchart LR
    subgraph Users["Platform Users"]
        ST["Student / Reviewer / Admin"]
    end

    subgraph Frontend["Next.js 16 Frontend (Vercel)"]
        MW["middleware.ts (Supabase SSR & RBAC)"]
        UI["App Router Pages (React 19, Tailwind v4)"]
    end

    subgraph Backend["FastAPI Backend (Render / Docker)"]
        SEC["security.py (JWT + RoleChecker)"]
        MOD["14 Domain Routers (/api/v1/*)"]
        ENG["Deterministic Engines (Eligibility + ChangeLens)"]
        DOC["Document Service (PyMuPDF + Tesseract + python-docx)"]
        AI["OpenAIProvider (gpt-4o / gpt-4o-mini)"]
    end

    subgraph Data["Supabase Platform"]
        AUTH["Supabase Auth (/auth/v1/user)"]
        PG[("PostgreSQL 16 (22 Tables, JSONB)")]
        STOR["Supabase Storage (Configured Buckets)"]
    end

    ST --> MW --> UI
    UI <--> AUTH
    UI -->|"HTTPS REST + Bearer JWT"| SEC
    SEC -->|"Verify JWT"| AUTH
    SEC --> MOD
    MOD --> ENG
    MOD --> DOC
    MOD --> AI
    MOD -->|"SQLAlchemy 2.0 Async"| PG
    DOC -.->|"Upload SDK pending"| STOR
```

---

## ChangeLens Workflow

```mermaid
flowchart TD
    A["Two Approved SchemeVersions"] --> B["POST /api/v1/policy-comparisons"]
    B --> C["Load Approved SchemeRule Rows"]
    C --> D["PolicyComparisonEngine.compare()"]
    D --> E["Index by (rule_category, rule_key)"]
    E --> F["ADDED / REMOVED / MODIFIED"]
    F --> G["Severity: HIGH / MEDIUM / LOW"]
    G --> H["Persist PolicyComparison + PolicyChangeEvent with Source Evidence"]
```

---

## Technology Stack

| Layer | Technologies (Verified from Manifests) |
|---|---|
| **Frontend** | Next.js `16.4.6`, React `19.3.0`, TypeScript `^5`, Tailwind CSS `4.3.3`, `@supabase/ssr`, `@supabase/supabase-js`, `axios`, `zod`, `react-hook-form`, `lucide-react`, `recharts`, `framer-motion` |
| **Backend** | Python `3.10+` (`3.11` in Docker/CI), FastAPI `0.115.0`, Uvicorn `0.32.0`, Pydantic `2.10.0`, SQLAlchemy `2.0.36` (async), `asyncpg`, Alembic `1.14.0`, `structlog` |
| **Document & OCR** | `PyMuPDF==1.25.0`, `pytesseract==0.3.13`, `Pillow==11.0.0`, `python-docx==1.1.2`, `beautifulsoup4==4.12.3` |
| **AI** | `openai==1.57.0` (`gpt-4o`, `gpt-4o-mini`), `tiktoken==0.8.0` (`anthropic==0.40.0` listed in `requirements.txt`, provider not yet implemented) |
| **Database / Auth / Hosting** | Supabase (PostgreSQL 16, Auth, Storage), Vercel (`sin1`), Render (`singapore`), Docker & GitHub Actions |

---

## System Requirements

- **Python**: `3.10+` (`3.11` used in Docker and CI)
- **Node.js**: `20+` and `npm`
- **Database & Auth**: Supabase project (or local PostgreSQL 16 via Docker)
- **Optional**: OpenAI API key (AI features degrade gracefully without it), Tesseract OCR binary for scanned PDFs, Docker Desktop

---

## Installation and Setup

### Automated Bootstrap (macOS / Linux / Git Bash)

```bash
git clone https://github.com/saipraveen-k/niyamdrishti.git
cd niyamdrishti
bash scripts/setup.sh
```

### Manual Setup (Windows PowerShell / Cross-Platform)

```bash
# Backend
cd backend
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1 | macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Frontend
cd ../frontend
npm install
cp .env.example .env.local
```

---

## Environment Configuration

Configure `backend/.env` (see [docs/07-development/ENVIRONMENT_VARIABLES.md](docs/07-development/ENVIRONMENT_VARIABLES.md)):

```env
APP_ENV=development
DEBUG=true
SECRET_KEY=CHANGE_ME_TO_A_LONG_RANDOM_STRING_AT_LEAST_32_CHARS
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
DATABASE_URL=postgresql+asyncpg://postgres:your-password@db.your-project.supabase.co:5432/postgres
OPENAI_API_KEY=sk-...
ALLOWED_ORIGINS=http://localhost:3000
```

Configure `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

---

## Running the Application

```bash
# 1. Seed 4 representative schemes (after DB tables exist)
cd backend
python -m scripts.seed_schemes

# 2. Start FastAPI backend
uvicorn app.main:app --reload

# 3. Start Next.js frontend (in a separate terminal)
cd frontend
npm run dev
```

Or run the local container stack (`api`, `frontend`, `postgres`, optional `redis`):

```bash
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend Health: `http://localhost:8000/health`
- Swagger UI (dev only): `http://localhost:8000/api/docs`

---

## Testing Instructions

```bash
# Backend unit & smoke tests (uses SQLite in-memory via tests/conftest.py)
cd backend
pytest -v

# Frontend TypeScript & ESLint checks
cd frontend
npx tsc --noEmit
npm run lint
```

Observed results on **2026-11-25**: `pytest` **33 passed, 2 failed** (`test_compound_and_all_pass`, `test_compound_or_one_passes`); `npx tsc --noEmit` **passed**; `npm run lint` **27 problems (9 errors, 18 warnings)**. See [docs/08-testing-and-quality/TEST_RESULTS.md](docs/08-testing-and-quality/TEST_RESULTS.md).

---

## Screenshots

No screenshots are committed in the repository yet. See the [Screenshot Checklist & Capture Guide](docs/assets/README.md) for the 10 recommended views and local capture steps.

---

## Project Directory Structure

```text
NiyamDrishti/
├── .github/workflows/ci.yml    # GitHub Actions CI (pytest, tsc, build, pip-audit)
├── backend/
│   ├── app/
│   │   ├── ai/                 # AIProvider ABC, OpenAIProvider, Extraction schemas
│   │   ├── core/               # config, logging, permissions, security
│   │   ├── database/           # asyncpg session, JSONB type, 22 models, Alembic env
│   │   ├── modules/            # 14 FastAPI modules (eligibility, changelens, schemes, etc.)
│   │   └── workers/            # Empty worker stub
│   ├── scripts/seed_schemes.py # Seeds 4 AP/Telangana/All-India schemes
│   ├── tests/                  # Pytest unit & health test suite
│   ├── Dockerfile              # Multi-stage Python 3.11 + Tesseract + Poppler
│   └── render.yaml             # Render service & Postgres blueprint
├── frontend/
│   ├── src/app/                # Next.js 16 App Router pages
│   ├── src/components/         # UI primitives, layout, feature cards
│   ├── src/hooks/              # useAuth, useSchemes, useScheme
│   ├── src/lib/                # apiClient, Supabase browser/server clients
│   └── vercel.json             # Security headers & /api/* rewrite
├── docs/                       # Complete structured documentation & Mermaid diagrams
├── scripts/setup.sh            # Local setup script
└── docker-compose.yml          # Local stack
```

---

## Team Members & Individual Contributions

> [!NOTE]
> The contribution percentages below are **team-provided indicative estimates**, not measured repository statistics.

| Team Member | Role & Responsibilities | Indicative Contribution *(Team Estimate)* |
|---|---|---:|
| **Sai Praveen Korubilli** | Project Lead, System Architecture, AI, Core Backend, Eligibility Engine, ChangeLens, and Integration | 40% |
| **Susanna Hebzibah Posupo** | Frontend Development and UI Integration | 15% |
| **Doddipatla Laxmi Lalitha Raja Aparna** | Backend Development and API Integration | 15% |
| **Chipparla Siva Rama Teja** | Government Scheme Research, Data Preparation, and Documentation | 10% |
| **Chandaka Jogiraju** | Quality Assurance, Functional Testing, and Validation | 10% |
| **Ramakoti Sruthi Alekhya** | Functional Testing, Scheme Research, and Presentation | 10% |

See [Team Overview](docs/10-team-and-project/TEAM_OVERVIEW.md) and [Individual Contributions](docs/10-team-and-project/INDIVIDUAL_CONTRIBUTIONS.md).

---

## Security & Privacy

- **Authentication**: Supabase Auth JWT verification via `/auth/v1/user` and 5-role RBAC (`RoleChecker`).
- **Upload Protection**: 20 MB cap, MIME allowlist, binary magic-byte inspection, SHA-256 hashing, and 200-page PDF cap.
- **Privacy**: Does not collect Aadhaar numbers or bank details; caste category and PwD fields are optional and marked user-declared.

---

## Known Limitations

- `EligibilityEngine._evaluate_compound()` has a field-mapping bug causing 2 compound-rule unit tests to fail.
- Background document processing (`app/workers/`), Supabase Storage upload SDK calls, `StudentImpact` computation, and RAG vector retrieval are not yet wired.
- Frontend pages for `/changelens`, `/lifemap`, `/applications`, `/assistant`, and `/eligibility` have API route/schema mismatches with backend routers.
- Alembic `versions/` has no migration scripts yet and `env.py` has stale imports.

See [docs/08-testing-and-quality/KNOWN_LIMITATIONS.md](docs/08-testing-and-quality/KNOWN_LIMITATIONS.md) for the complete list.

---

## Future Roadmap

1. Fix `EligibilityEngine._evaluate_compound()` and align frontend–backend API contracts.
2. Fix `Alembic` `env.py` imports and generate the baseline migration.
3. Implement `app/workers/` background extraction loop + Supabase Storage uploads.
4. Implement automated `StudentImpact` computation and RAG vector citations for `/assistant/chat`.
5. Build missing frontend routes (`/admin/*`, `/coordinator`, `/notifications`, `/about`, `/privacy`, `/terms`).

---

## Documentation Navigation

| Category | Entry Point |
|---|---|
| **Documentation Hub** | [docs/README.md](docs/README.md) |
| **Codebase Audit** | [docs/PROJECT_AUDIT.md](docs/PROJECT_AUDIT.md) |
| **Overview & Problem** | [docs/01-overview/PROJECT_OVERVIEW.md](docs/01-overview/PROJECT_OVERVIEW.md) |
| **Product & Workflows** | [docs/02-product/PRODUCT_FEATURES.md](docs/02-product/PRODUCT_FEATURES.md) |
| **System Architecture** | [docs/03-architecture/SYSTEM_ARCHITECTURE.md](docs/03-architecture/SYSTEM_ARCHITECTURE.md) |
| **Technical & Security** | [docs/04-technical/TECHNOLOGY_STACK.md](docs/04-technical/TECHNOLOGY_STACK.md) |
| **Database & API Reference** | [docs/05-database-and-api/API_REFERENCE.md](docs/05-database-and-api/API_REFERENCE.md) |
| **AI & Algorithms** | [docs/06-ai-and-intelligence/AI_OVERVIEW.md](docs/06-ai-and-intelligence/AI_OVERVIEW.md) |
| **Development Setup** | [docs/07-development/GETTING_STARTED.md](docs/07-development/GETTING_STARTED.md) |
| **Testing & Limitations** | [docs/08-testing-and-quality/TEST_RESULTS.md](docs/08-testing-and-quality/TEST_RESULTS.md) |
| **Deployment & CI/CD** | [docs/09-deployment-and-devops/DEPLOYMENT_OVERVIEW.md](docs/09-deployment-and-devops/DEPLOYMENT_OVERVIEW.md) |
| **Team & Roadmap** | [docs/10-team-and-project/TEAM_OVERVIEW.md](docs/10-team-and-project/TEAM_OVERVIEW.md) |
| **Hackathon Pitch & Demo** | [docs/11-hackathon/HACKATHON_OVERVIEW.md](docs/11-hackathon/HACKATHON_OVERVIEW.md) |
| **Mermaid Diagrams** | [docs/diagrams/system-architecture.mmd](docs/diagrams/system-architecture.mmd) |
| **Docs Quality Status** | [docs/DOCUMENTATION_STATUS.md](docs/DOCUMENTATION_STATUS.md) |

---

## License

No `LICENSE` file is currently present in this repository.
