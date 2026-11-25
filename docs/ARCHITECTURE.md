# Architecture

## System overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                             │
│  Next.js 16 (Vercel)  ←── Supabase Auth ───► Supabase DB  │
│  React 19 / Tailwind                                        │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS (REST)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Render)                      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Eligibility │  │  ChangeLens  │  │  AI Assistant    │  │
│  │  Engine      │  │  Comparison  │  │  (RAG / Chat)    │  │
│  │  (pure Python│  │  Engine      │  │                  │  │
│  │  no AI)      │  │  (pure Python│  │  OpenAI / Claude │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  SQLAlchemy 2.0 async (asyncpg)                     │    │
│  └───────────────────────┬─────────────────────────────┘    │
└──────────────────────────┼──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
      ┌───────▼───────┐        ┌────────▼────────┐
      │  PostgreSQL   │        │ Supabase Storage │
      │  (Supabase)   │        │ (official docs / │
      │  JSONB rules  │        │  student uploads)│
      └───────────────┘        └─────────────────┘
```

---

## Core design principles

### 1. Deterministic evaluation, AI extraction

The eligibility engine (`app/modules/eligibility/engine.py`) and comparison engine (`app/modules/changelens/comparison_engine.py`) are pure Python — no LLM calls. This guarantees:

- Reproducible results for the same input
- Auditable logic (every rule evaluation has an explanation string)
- No hallucinated pass/fail decisions

LLMs are only used to **extract and structure** rules from PDF documents into a machine-readable JSONB condition format. Human reviewers then approve or reject extracted rules before they go live.

### 2. Rule condition schema

Extracted eligibility rules are stored as JSONB in `scheme_rules.condition`:

```json
{
  "operator": "lte",
  "value": 300000,
  "unit": "inr",
  "note": "Annual family income limit"
}
```

Compound rules use `logic` + `sub_conditions`:

```json
{
  "logic": "or",
  "sub_conditions": [
    { "operator": "eq", "value": "SC" },
    { "operator": "eq", "value": "ST" }
  ]
}
```

Supported operators: `lte`, `lt`, `gte`, `gt`, `eq`, `neq`, `in`, `not_in`.

### 3. Schema versioning

Every uploaded official document creates a new `SchemeVersion`. Rules are attached to versions, not directly to the scheme. The `Scheme.latest_version_id` denormalisation provides fast listing without joining on versions.

Policy comparisons (`PolicyComparison`) record the diff between two approved versions as `PolicyChangeEvent` rows, persisted for audit trails.

### 4. Auth model

Authentication is entirely delegated to Supabase Auth (JWT). The FastAPI backend validates tokens by calling Supabase's `/auth/v1/user` endpoint. No password hashing in the application layer.

Role-based access control is implemented in `app/core/permissions.py` using a `require_roles()` FastAPI dependency.

### 5. AI provider abstraction

`app/ai/providers/base.py` defines an abstract `AIProvider` interface. `openai_provider.py` implements it for OpenAI. Adding Anthropic or any other provider requires implementing the interface and updating the factory in `app/core/config.py`. The switch is controlled by the `AI_PROVIDER` env var.

---

## Database models

| Table | Purpose |
|---|---|
| `schemes` | Master scheme record (denormalized summary) |
| `scheme_sources` | Official source documents / URLs |
| `scheme_versions` | Versioned rule snapshots per document upload |
| `scheme_documents` | Uploaded PDFs stored in Supabase Storage |
| `scheme_rules` | Individual extracted eligibility rules (JSONB condition) |
| `policy_comparisons` | Recorded comparisons between two versions |
| `policy_change_events` | Per-rule change events from a comparison |
| `users` | App user records (linked to Supabase Auth UID) |
| `applications` | Student application records |
| `documents` | Student-uploaded support documents |

---

## Module structure

```
app/modules/
├── auth/           JWT token validation, role extraction
├── users/          User profile CRUD
├── profiles/       Student academic/demographic profile
├── schemes/        Scheme listing, search, bookmarks
├── eligibility/    Rule evaluation engine + router
├── documents/      PDF upload, OCR, extraction trigger
├── changelens/     Comparison engine + router
├── impact/         Impact assessment (planned Phase 9)
├── lifemap/        Action plan generation and tracking
├── applications/   Student application status tracking
├── assistant/      RAG chatbot with document citations
├── reviews/        Human review queue for extracted rules
├── notifications/  Email/in-app notification stubs
└── monitoring/     Admin health check, job listing
```

---

## Data flow: document → live rules

```
Admin uploads PDF
        │
        ▼
Document stored in Supabase Storage
        │
        ▼
Background worker: OCR + text extraction (PyMuPDF + Tesseract)
        │
        ▼
LLM extraction: text → structured SchemeRule JSONB conditions
        │
        ▼
SchemeVersion created (is_approved=false)
        │
        ▼
Reviewer queue: human approves/rejects each rule
        │
        ▼
SchemeVersion marked is_approved=true, is_active=true
        │
        ▼
Scheme.latest_version_id updated
        │
        ▼
Students can now run eligibility checks against the new rules
```
