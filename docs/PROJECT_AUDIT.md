# NiyamDrishti — Project Audit

**Audit Date:** 2026-11-25
**Auditor:** Principal Software Architect (AI-assisted)
**Status:** Greenfield — fresh build initiated

---

## 1. Current Project Architecture

### Repository State

The repository at `c:/tempp/projects/NiyamDrishti` was inspected on 2026-11-25.

**Finding:** The repository contains only `.claude/settings.local.json` — it is effectively empty.
No prior frontend, backend, database schema, authentication layer, tests, or deployment configuration exists.

This audit documents the architecture as *designed and initiated* rather than as found.

---

## 2. Existing Working Features

**None.** This is a greenfield project.

---

## 3. Existing Incomplete Features

**None.** No prior code exists.

---

## 4. Bugs and Technical Debt

**None pre-existing.** All technical debt will be introduced and tracked from this build.

---

## 5. Components Worth Preserving

**None to preserve.** All components are being created fresh.

---

## 6. Missing Requirements (Initial State)

The following complete feature set must be built from scratch:

| Feature Area | Status |
|---|---|
| Next.js frontend application | Scaffolded — to be built |
| FastAPI backend application | Directory structure created — to be built |
| Supabase PostgreSQL schema | To be created |
| Supabase Auth integration | To be created |
| Supabase Storage buckets | To be created |
| Student onboarding and profiles | To be created |
| Scheme discovery and filtering | To be created |
| Deterministic eligibility engine | To be created |
| Document upload and processing | To be created |
| OCR extraction pipeline | To be created |
| ChangeLens policy comparison | To be created |
| Personalized Impact Engine | To be created |
| LifeMap action planning | To be created |
| AI assistant with grounding | To be created |
| Multilingual support (EN/TE/HI) | To be created |
| Role-based dashboards (5 roles) | To be created |
| Row Level Security policies | To be created |
| Background job processing | To be created |
| PDF report generation | To be created |
| CI/CD pipelines | To be created |
| Tests (unit, API, E2E, security) | To be created |
| Deployment configuration | To be created |

---

## 7. Proposed Implementation Sequence

### Phase 0 (Complete)
- Repository inspection
- Architecture documentation
- Environment scaffolding

### Phase 1 (In Progress)
- Core backend structure (FastAPI, config, security, models)
- Core frontend structure (Next.js, design system, layout)
- Database schema design
- Environment configuration

### Phase 2
- Supabase Auth integration
- JWT validation middleware
- Student registration and login flow
- Google OAuth integration
- Phone OTP (documented as requiring provider configuration)
- Role assignment system

### Phase 3
- Five role-based dashboards
- Student onboarding form
- Student profile storage
- Role-based route guards

### Phase 4
- Verified scheme catalogue (AP/Telangana/Central)
- Scheme search, filter and discovery
- Deterministic eligibility calculations
- Match explanations and scoring
- Bookmarking and comparison

### Phase 5
- Private document uploads (Supabase Storage)
- File validation (format, size, magic bytes)
- SHA-256 hashing and deduplication
- PDF/DOCX/image text extraction
- OCR for scanned documents
- Background processing queue

### Phase 6 — ChangeLens
- LLM-assisted rule extraction
- Pydantic structured output validation
- Document reviewer approval workflow
- Side-by-side rule comparison
- Evidence-linked change reporting
- PDF comparison report generation

### Phase 7 — Impact Engine
- Per-student eligibility re-evaluation
- Old vs new rule outcome comparison
- Criterion-level passed/failed/unknown results
- Synthetic profile simulation

### Phase 8 — LifeMap and AI Assistant
- Personalized action plan generation
- Document checklist
- Application deadline tracking
- Alternative scheme recommendations
- Grounded multilingual AI assistant
- Prompt injection protection

### Phase 9 — Security and QA
- RLS policy implementation and testing
- Security testing (upload attacks, injection)
- Pytest suite
- Playwright E2E suite
- Deployment configuration (Vercel, Render)
- Production smoke tests

### Phase 10 — Hackathon Polish
- Demo data preparation
- Visualization refinement
- Architecture diagrams
- Documentation completion

---

## 8. Requirement-to-Implementation Checklist

### Functional Requirements

- [ ] Student registration and email verification
- [ ] Google OAuth login
- [ ] Phone OTP (requires SMS provider — Twilio/MSG91)
- [ ] Password reset flow
- [ ] Student profile creation and persistence
- [ ] Public scheme browsing (unauthenticated)
- [ ] Scheme search and filters
- [ ] Deterministic eligibility evaluation
- [ ] Eligibility match score with criterion breakdown
- [ ] Scheme bookmarking
- [ ] Scheme comparison
- [ ] Admin scheme management
- [ ] Document upload (PDF, DOCX, image, webpage)
- [ ] Document validation (magic bytes, size, page count)
- [ ] Document SHA-256 deduplication
- [ ] Background document processing
- [ ] OCR for scanned PDFs
- [ ] LLM rule extraction with Pydantic validation
- [ ] Reviewer approval workflow
- [ ] ChangeLens side-by-side comparison
- [ ] Evidence-linked change highlighting
- [ ] Personalized impact evaluation
- [ ] Per-criterion passed/failed/unknown display
- [ ] Synthetic profile simulation
- [ ] LifeMap action plan
- [ ] Document checklist
- [ ] Application status tracking (manual)
- [ ] AI assistant with grounded responses
- [ ] Multilingual explanations (EN/TE/HI)
- [ ] PDF report download (comparison + action plan)
- [ ] Admin dashboard
- [ ] Super Admin dashboard
- [ ] Reviewer dashboard
- [ ] College Coordinator dashboard
- [ ] Notifications
- [ ] Audit logging

### Security Requirements

- [ ] Server-side RBAC
- [ ] Supabase RLS on all tables
- [ ] Private document storage
- [ ] Signed URL expiry
- [ ] Upload validation (format + magic bytes)
- [ ] Prompt injection protection
- [ ] Rate limiting
- [ ] Login attempt restrictions
- [ ] Audit log for privileged actions
- [ ] No secrets in code/CI logs
- [ ] CORS restricted to approved origins
- [ ] Account deletion with data cleanup
- [ ] Personal data export

### Quality Requirements

- [ ] Unit tests (eligibility, comparison logic)
- [ ] API tests (all endpoints)
- [ ] RLS tests (cross-user isolation)
- [ ] Frontend component tests
- [ ] E2E tests (Playwright)
- [ ] Mobile and desktop layout verification
- [ ] No inert buttons or placeholder workflows

### Deployment Requirements

- [ ] Vercel frontend deployment
- [ ] Render backend deployment
- [ ] Supabase database migrations
- [ ] Storage bucket policies
- [ ] Environment variable configuration
- [ ] Health check endpoints
- [ ] CI/CD pipelines
- [ ] Production smoke tests

---

## 9. Technology Stack (Confirmed)

| Layer | Technology |
|---|---|
| Frontend | Next.js 16+, TypeScript, Tailwind CSS |
| Backend | Python 3.10+, FastAPI 0.16+, Pydantic v2 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | Supabase PostgreSQL |
| Auth | Supabase Auth |
| Storage | Supabase Storage |
| Background Jobs | PostgreSQL-backed queue (async worker loop) |
| AI Provider | OpenAI / Anthropic (abstracted) |
| OCR | Tesseract via pytesseract |
| PDF Processing | PyMuPDF |
| Testing Backend | Pytest, pytest-asyncio |
| Testing Frontend | Jest, React Testing Library, Playwright |
| Deployment | Vercel (frontend), Render (backend) |
| CI/CD | GitHub Actions |

---

## 10. Known Constraints and Limitations

### Phone OTP
- Requires a configured SMS provider (Twilio, MSG91 or Supabase Phone Auth)
- Not functional without provider credentials
- Interface implemented; activation requires credentials

### AI Features
- Require OPENAI_API_KEY or ANTHROPIC_API_KEY
- Degrade gracefully when credentials absent
- Not free — costs accrue per token

### OCR
- Tesseract requires system installation
- Production container must include Tesseract binary
- Accuracy depends on document quality

### Free-tier Hosting Constraints
- Render free tier has sleep behaviour (cold starts)
- Supabase free tier has row limits and storage limits
- Documented in DEPLOYMENT.md

### Document Retention
- Default retention: 30 days (configurable)
- Must be confirmed against institutional and legal requirements before production

---

*This document is updated as each development phase completes.*
