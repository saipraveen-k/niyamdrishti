# NiyamDrishti — Project Audit

> **Audit Date:** 2026-11-25  
> **Scope:** Full static inspection of the actual repository (`frontend/`, `backend/`, `.github/`, `docker-compose.yml`, `scripts/`, `docs/`) plus live execution of `pytest` and `tsc` / `eslint`.  
> **Purpose:** Document the **exact current implementation state** of NiyamDrishti without claiming unbuilt features as complete.

---

## 1. Project Overview

**NiyamDrishti** is an AI-assisted government policy intelligence and personalized student scholarship discovery platform targeting Andhra Pradesh, Telangana, and All India / Central schemes.

Its core architectural thesis is **deterministic evaluation paired with human-verified AI extraction**:

- **AI (`OpenAIProvider`)** extracts structured rules from official notifications (PDF/DOCX/image) into Pydantic-validated JSONB conditions (`ExtractedSchemeRules`), and powers a multilingual (`en` / `te` / `hi`) conversational assistant.
- **Human reviewers** (`document_reviewer`, `admin`, `super_admin`) approve or reject extracted rules before they become active.
- **Pure Python engines** (`EligibilityEngine` and `PolicyComparisonEngine`) deterministically evaluate student eligibility and compute rule-level diffs between scheme versions without LLM guessing.

---

## 2. Existing Implementation Status

The repository contains an active initial codebase across `frontend/` (Next.js 16 App Router) and `backend/` (FastAPI + SQLAlchemy 2.0 async), with 4 git commits on the repository history. However, several modules are **scaffolded, partially wired, or contain contract mismatches** between the frontend and backend.

| Status Category | Summary |
|---|---|
| **Implemented & Tested** | `PolicyComparisonEngine` (14/14 unit tests pass), core FastAPI health/root/OpenAPI smoke checks (5/5 pass), `EligibilityEngine` single-rule & score logic (13/15 pass; 2 compound-rule tests fail). |
| **Implemented (Not Integration-Tested)** | SQLAlchemy 2.0 async ORM (22 tables), Supabase JWT validation (`verify_supabase_token`), RBAC `RoleChecker`, `schemes` CRUD/filtering/bookmarking, `profiles` CRUD, `eligibility/evaluate` endpoint, `policy-comparisons` POST/GET endpoints, `reviews` queue/approve endpoints, `applications` CRUD + status history, `lifemap` action plan creation, `documents/service.py` (magic bytes, SHA-256, PyMuPDF, Tesseract, python-docx), `OpenAIProvider`, `seed_schemes.py` (4 schemes), Next.js landing, auth, dashboard, scheme discovery, and feature UI pages. |
| **Partially Implemented / Mismatched** | Frontend–backend API route/payload contracts on `changelens`, `lifemap`, `applications`, `assistant`, and `eligibility` pages; `documents/upload` queues a DB job without uploading bytes to Supabase Storage; `assistant/chat` uses direct LLM chat without vector/RAG retrieval; `SchemeSearchParams.max_income` and `min_marks` accepted in router but not filtered in `SchemeService`; `Alembic` has no migration files and stale imports in `env.py`. |
| **Planned / Stubbed** | Background worker loop (`app/workers/__init__.py` is empty); `AnthropicProvider` implementation; automatic `StudentImpact` calculation on policy comparison; `notifications/me` and `admin/jobs` endpoints; Redis caching/rate-limiting; frontend subpages (`/about`, `/privacy`, `/terms`, `/forgot-password`, `/coordinator`, `/notifications`, `/settings`, `/admin/*`); frontend Jest/Playwright tests; Phone OTP. |

---

## 3. Architecture Findings

### What Is Built Cleanly

1. **Clear Modular Monolith (`backend/app/modules/`)**: 14 domain modules (`auth`, `users`, `profiles`, `schemes`, `eligibility`, `documents`, `changelens`, `impact`, `lifemap`, `applications`, `assistant`, `reviews`, `notifications`, `monitoring`) mounted under `/api/v1`.
2. **Cross-Dialect ORM (`app/database/types.py`)**: Custom `JSONB` `TypeDecorator` maps to PostgreSQL `JSONB` in production and `JSON` in SQLite for fast in-memory `pytest` execution.
3. **Provider Abstraction (`app/ai/providers/base.py`)**: `AIProvider` ABC cleanly separates `extract_structured`, `chat`, and `translate` from business logic.
4. **Prompt Injection Guardrails**: Both `OpenAIProvider.extract_structured()` (wrapping document text in `<document>` tags with explicit system instructions) and `assistant/router.py` enforce grounding boundaries.
5. **Security Headers & Auth Middleware**: `frontend/vercel.json` sets `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and `Permissions-Policy`; `frontend/src/middleware.ts` enforces Supabase session checks and role gates on `/admin`, `/reviewer`, and `/coordinator`.

### Critical Discrepancies Found in Code Inspection

1. ~~**Compound Condition Bug in `EligibilityEngine`**~~ — **Fixed**: compound `and`/`or` rules now inherit the parent rule's category/key, and `test_compound_and_all_pass` / `test_compound_or_one_passes` pass (all 15 eligibility tests green).
2. **Frontend–Backend API Contract Mismatches**:
   - **ChangeLens**: `frontend/src/app/changelens/page.tsx` calls `GET /changelens/compare/{scheme_id}`, while backend exposes `POST /api/v1/policy-comparisons` and `GET /api/v1/policy-comparisons/{comparison_id}`.
   - **LifeMap**: `frontend/src/app/lifemap/page.tsx` calls `GET /lifemap/plans` and `PATCH /lifemap/tasks/{task_id}`, while backend exposes `GET /api/v1/action-plans/me` and `POST /api/v1/action-plans`.
   - **Applications**: `frontend/src/app/applications/page.tsx` calls `GET /applications`, while backend exposes `GET /api/v1/applications/me`. Also, frontend status enum uses `not_started` / `in_progress`, while backend model uses `planning` / `documents_gathering`.
   - **AI Assistant**: `frontend/src/app/assistant/page.tsx` sends `{ session_id, message }` and reads `{ answer, citations }`, while backend `assistant/router.py` expects `{ messages, scheme_id, language }` and returns `{ reply, language, sources, disclaimer }`.
   - **Eligibility**: `frontend/src/app/eligibility/page.tsx` reads `report.criteria` and matches uppercase `"PASSED"` / `"FAILED"`, while backend returns `criterion_results` and lowercase `"passed"` / `"failed"`.
3. **Unwired Background Worker & Storage**:
   - `POST /api/v1/documents/upload` validates magic bytes and inserts `SchemeDocument` + `DocumentProcessingJob(status="queued")`, but does not upload file bytes to Supabase Storage, and `app/workers/__init__.py` is empty so queued jobs are never executed automatically.
4. **Alembic Migration Gap**:
   - `backend/app/database/migrations/versions/` contains only `.gitkeep` (no migration scripts).
   - `backend/app/database/migrations/env.py` imports non-existent classes (`User`, `Application`, `Document`) instead of the actual models in `app/database/models/__init__.py`.
5. **Redis Unused in Application Code**:
   - `docker-compose.yml` defines a `redis:7-alpine` service, but no Redis client library is in `requirements.txt` and no Python module connects to Redis.
6. **Anthropic Provider Not Implemented**:
   - `backend/app/core/config.py` includes `ai_provider: Literal["openai", "anthropic"]` and `anthropic_api_key`, and `requirements.txt` includes `anthropic==0.40.0`, yet `app/ai/providers/` only implements `OpenAIProvider`.

---

## 4. Feature Implementation Matrix

| Feature Area | Backend Status | Frontend Status | Test Status | Overall Classification |
|---|---|---|---|---|
| **Authentication (Supabase Email + Google OAuth)** | `verify_supabase_token` + `GET /auth/status` | Login, Register, OAuth callback, Middleware | Not tested | Implemented (needs E2E verification) |
| **RBAC (5 Roles)** | `RoleChecker`, `require_roles`, `AppRole` | `middleware.ts` + role-filtered `Sidebar` | Not tested | Implemented (needs API tests) |
| **User & Student Profiles** | `GET /users/me`, `GET/POST/PATCH /profiles` | `/settings/profile` form | Not tested | Implemented (no auto `user_profiles` trigger in repo) |
| **Scheme Discovery & Bookmarking** | `GET /schemes`, `GET /schemes/{id}`, `POST /bookmark`, Admin CRUD/publish | `/schemes`, `/schemes/[id]`, `SchemeCard` | Not tested | Implemented (`max_income`/`min_marks` filters unused) |
| **Deterministic Eligibility Engine** | `EligibilityEngine` + `POST /eligibility/evaluate` | `/eligibility` + `CriterionResult` | 13/15 unit tests pass (2 compound fail) | Implemented with known bug & UI mismatch |
| **ChangeLens Policy Comparison** | `PolicyComparisonEngine` + `POST/GET /policy-comparisons` | `/changelens` + `ChangeEventCard` | 14/14 unit tests pass | Implemented (backend tested; UI path mismatch) |
| **Document Upload & Validation** | `validate_upload`, magic bytes, SHA-256, `POST /documents/upload` | Linked from `/admin/documents` (page missing) | Not tested | Partially Implemented (no Storage upload) |
| **Text Extraction & OCR** | `extract_text_from_pdf`, `_ocr_pdf_pages`, `docx`, `image` | None | Not tested | Implemented in `service.py`, not invoked by worker |
| **LLM Rule Extraction** | `OpenAIProvider.extract_structured`, `ExtractedSchemeRules` | None | Not tested | Implemented in provider, not wired to job pipeline |
| **Background Job Queue** | `DocumentProcessingJob` & `Attempt` models | Linked from `/admin/jobs` (page missing) | Not tested | Partially Implemented (`workers/__init__.py` empty) |
| **Human Reviewer Queue** | `GET /reviews/queue`, `POST /reviews/{id}/approve` | `/reviewer` dashboard | Not tested | Implemented (needs API/UI testing) |
| **Personalized Impact Engine** | `StudentImpact` model + `GET /impacts/me` | Referenced on landing page | Not tested | Partially Implemented (no computation service) |
| **LifeMap Action Planning** | `ActionPlan`, `ActionTask`, `GET/POST /action-plans` | `/lifemap` page | Not tested | Partially Implemented (path & task-patch mismatch) |
| **Application Status Tracker** | `StudentApplication`, `History`, `GET/POST/PATCH` | `/applications` page | Not tested | Implemented (path & status enum mismatch) |
| **AI Assistant & Multilingual** | `POST /assistant/chat` (`OpenAIProvider`, EN/TE/HI) | `/assistant` chat UI | Not tested | Partially Implemented (no RAG retrieval; payload mismatch) |
| **Notifications & Monitoring** | `GET /notifications/me` (stub), `GET /admin/system-health`, `GET /admin/jobs` (stub) | `/admin` health card | Not tested | Partially Implemented / Stubbed |
| **College Coordinator Portal** | `College`, `CollegeMembership` models, `COORDINATOR_ROLES` | Sidebar link `/coordinator` (page missing) | Not tested | Planned / Models Only |
| **PDF Report Export** | `report_storage_path` columns on `PolicyComparison` & `ActionPlan` | Not implemented | Not tested | Planned |
| **Phone OTP** | Mentioned in `.env.example` comments | Not implemented | Not tested | Planned (requires SMS provider) |

---

## 5. Technology Stack Summary

| Layer | Technologies (Verified from Manifests) |
|---|---|
| **Frontend** | Next.js `16.4.6`, React `19.3.0`, TypeScript `^5`, Tailwind CSS `4.3.3`, `@supabase/ssr` `^0.12.7`, `@supabase/supabase-js` `^2.119.2`, `axios` `^1.21.1`, `zod` `^4.6.7`, `react-hook-form` `^7.92.0`, `lucide-react` `^1.80.0`, `recharts` `^3.11.1`, `framer-motion` `^14.14.0` |
| **Backend** | Python `3.10+` (`3.11` in Docker/CI), FastAPI `0.115.0`, Uvicorn `0.32.0`, Starlette `0.41.0`, Pydantic `2.10.0`, pydantic-settings `2.6.0`, structlog `24.4.0`, httpx `0.28.0` |
| **Database & ORM** | PostgreSQL `16` (Supabase / Docker `postgres:16-alpine`), SQLAlchemy `2.0.36` async, asyncpg `0.30.0`, Alembic `1.14.0` |
| **Auth & Storage** | Supabase Auth (JWT via `/auth/v1/user`), Supabase Storage (`supabase==2.10.0` SDK installed) |
| **Document & OCR** | `PyMuPDF==1.25.0`, `pytesseract==0.3.13`, `Pillow==11.0.0`, `python-docx==1.1.2`, `beautifulsoup4==4.12.3`, `lxml==5.3.0` |
| **AI** | `openai==1.57.0` (`gpt-4o-mini` / `gpt-4o` defaults), `tiktoken==0.8.0`; `anthropic==0.40.0` installed but no provider class |
| **Testing & QA** | `pytest` (`8.3.3` in manifest, `9.2.0` in venv), `pytest-asyncio`, `pytest-cov`, `eslint` `^9`; `jest` & `@playwright/test` installed without test files |
| **Deployment & CI** | Vercel (`frontend/vercel.json`), Render (`backend/render.yaml`), Docker (`backend/Dockerfile`, `docker-compose.yml`), GitHub Actions (`.github/workflows/ci.yml`) |

---

## 6. Database Overview

The SQLAlchemy metadata defines **22 tables** across 4 model modules:

- **Users & Institutions (`models/user.py`)**: `user_profiles`, `student_profiles`, `colleges`, `college_memberships`, `admin_invitations`
- **Schemes & Policy Intelligence (`models/scheme.py`)**: `schemes`, `scheme_sources`, `scheme_versions`, `scheme_documents`, `scheme_rules`, `policy_comparisons`, `policy_change_events`
- **Documents & Job Queue (`models/document.py`)**: `document_uploads`, `document_processing_jobs`, `document_processing_attempts`
- **Student Workflows (`models/application.py`)**: `student_scheme_evaluations`, `saved_schemes`, `student_impacts`, `action_plans`, `action_tasks`, `student_applications`, `application_status_history`

See [Database Schema](05-database-and-api/DATABASE_SCHEMA.md) and [Entity Relationship](05-database-and-api/ENTITY_RELATIONSHIP.md) for full column and relationship details.

---

## 7. API Overview

- **Base URL prefix**: `/api/v1` (plus `/` and `/health` at root)
- **Interactive OpenAPI docs**: `/api/docs`, `/api/redoc`, `/api/openapi.json` (disabled when `APP_ENV=production`)
- **Total implemented routes**: 25 HTTP endpoints across 14 routers (including 2 root endpoints and 2 stub endpoints).

See [API Reference](05-database-and-api/API_REFERENCE.md) for the exact endpoint catalog.

---

## 8. Security Observations

| Area | Observation |
|---|---|
| **Authentication** | Delegates credential handling to Supabase Auth; backend validates Bearer JWTs remotely via `GET {SUPABASE_URL}/auth/v1/user`. |
| **Authorization (RBAC)** | Server-side `require_roles(...)` enforces roles on admin, reviewer, and ChangeLens endpoints using `user_metadata.app_role`. |
| **Upload Security** | `validate_upload()` verifies size (`<= 20 MB`), MIME allowlist, and magic bytes (`%PDF`, `PK\x03\x04`, JPEG, PNG, WebP), plus SHA-256 hashing. |
| **Prompt Injection Defense** | `OpenAIProvider.extract_structured()` wraps document text in `<document>` delimiters and instructs the model to ignore embedded instructions. |
| **Gaps Observed** | No rate limiting middleware (`LOGIN_MAX_ATTEMPTS` in `config.py` is not enforced); no Supabase SQL RLS policy files are committed in the repo; `frontend/src/lib/api-client.ts` stores `nd_access_token` in `localStorage`; `monitoring/router.py` hardcodes `"database": "connected"` rather than executing a live DB probe; `require_self_or_roles` in `security.py` is defined but unused. |

---

## 9. Testing Status

Observed command outputs on **2026-11-25**:

- **Backend (`pytest -v`)**: **35 collected — 33 passed, 2 failed** (`0.44s`).
  - `tests/test_comparison_engine.py`: 14/14 passed.
  - `tests/test_health.py`: 5/5 passed.
  - `tests/test_sanity.py`: 1/1 passed.
  - `tests/test_eligibility_engine.py`: 13/15 passed; `test_compound_and_all_pass` and `test_compound_or_one_passes` failed.
- **Frontend TypeScript (`npx tsc --noEmit`)**: **Passed** (exit code 0, 0 errors).
- **Frontend ESLint (`npm run lint`)**: **Failed** (exit code 1 — 27 problems: 9 errors, 18 warnings).
- **Frontend Unit/E2E Tests**: None written (`jest` and `@playwright/test` are declared in `devDependencies` with no test suites or npm test scripts).

---

## 10. Known Limitations & Documentation Gaps

- **Known Limitations**: Documented in full in [Known Limitations](08-testing-and-quality/KNOWN_LIMITATIONS.md).
- **Pre-Audit Documentation Gaps**: Prior to this documentation overhaul, the repository only contained an outdated greenfield `PROJECT_AUDIT.md`, high-level `ARCHITECTURE.md`, `DEPLOYMENT.md`, `KNOWN_LIMITATIONS.md`, and root `README.md` — lacking API references, database schema docs, AI pipeline docs, development guides, testing reports, team records, hackathon materials, and Mermaid diagrams.

---

*Related: [Documentation Hub](README.md) · [Documentation Status](DOCUMENTATION_STATUS.md) · [Known Limitations](08-testing-and-quality/KNOWN_LIMITATIONS.md)*
