# Documentation Status

> **Last Verified:** 2026-11-25  
> **Scope:** Complete audit and validation of NiyamDrishti Markdown documentation, Mermaid diagrams, internal links, and repository claims.

---

## 1. Documentation Inventory Summary

| Metric | Observed Count / Status |
|---|---|
| **Total Markdown Files** | **87** (`README.md`, `frontend/README.md`, and **85** files under `docs/`) |
| **Standalone Mermaid Diagrams (`.mmd`)** | **10** files under `docs/diagrams/` |
| **Embedded Mermaid Blocks + Standalone `.mmd`** | **51** total Mermaid diagrams validated |
| **Internal Relative Links Checked** | **365** links verified across `README.md` and `docs/**/*.md` |
| **Broken Links / Missing Images** | **0** (after final validation pass) |
| **Secret Exposure Scan** | **0** leaked API keys or JWTs detected |

---

## 2. Mermaid Diagrams Created (`docs/diagrams/`)

| # | File | Diagram Type | Topic |
|---|---|---|---|
| 1 | [system-architecture.mmd](diagrams/system-architecture.mmd) | `flowchart LR` | Full-stack architecture (Next.js, FastAPI, Supabase, OpenAI, unused Redis) |
| 2 | [student-workflow.mmd](diagrams/student-workflow.mmd) | `flowchart TD` | Student registration to LifeMap & application tracking |
| 3 | [admin-workflow.mmd](diagrams/admin-workflow.mmd) | `flowchart TD` | Admin scheme creation, upload, review, publishing & ChangeLens |
| 4 | [changelens-workflow.mmd](diagrams/changelens-workflow.mmd) | `flowchart TD` | Version comparison & severity classification workflow |
| 5 | [ai-document-processing.mmd](diagrams/ai-document-processing.mmd) | `flowchart TD` | File validation, PyMuPDF/OCR/DOCX, OpenAI extraction, HITL gate |
| 6 | [eligibility-engine.mmd](diagrams/eligibility-engine.mmd) | `flowchart TD` | Deterministic `EligibilityEngine` evaluation & known compound bug note |
| 7 | [database-er.mmd](diagrams/database-er.mmd) | `erDiagram` | All 22 actual SQLAlchemy tables and relationships |
| 8 | [authentication-flow.mmd](diagrams/authentication-flow.mmd) | `sequenceDiagram` | Supabase Auth, Next.js middleware, and FastAPI JWT/RBAC checks |
| 9 | [deployment-architecture.mmd](diagrams/deployment-architecture.mmd) | `flowchart LR` | GitHub, CI, Vercel, Render, Supabase, and local Redis distinction |
| 10 | [ci-cd-pipeline.mmd](diagrams/ci-cd-pipeline.mmd) | `flowchart LR` | Exact `.github/workflows/ci.yml` jobs (checks only, no automated CD) |

### Mermaid Syntax Validation Status

- Validated all **51** Mermaid blocks (41 embedded in Markdown + 10 standalone `.mmd` files):
  - All diagram headers use valid GitHub-supported Mermaid types (`flowchart`, `sequenceDiagram`, `erDiagram`, `stateDiagram-v2`, `journey`, `pie`, `mindmap`, `gitGraph`).
  - Zero HTML `<br>` tags inside node labels.
  - Zero unquoted parentheses inside `[...]` bracket node labels.
  - Balanced `subgraph` / `end` blocks across all flowcharts.

---

## 3. Screenshots Available & Missing

- **Available Screenshots**: `0`
- **Missing Screenshots**: `10` recommended views tracked in [docs/assets/README.md](assets/README.md) (`/`, `/dashboard`, `/schemes`, `/eligibility`, `/changelens`, `/lifemap`, `/assistant`, `/admin`, `/reviewer`, mobile responsive view).
- **Placeholder Directories Ready**: `docs/assets/images/`, `docs/assets/screenshots/`, `docs/assets/architecture/`.

---

## 4. Documentation Gaps & Features Needing Code-Level Work / Verification

The following items are accurately documented as incomplete or needing runtime verification rather than being marked finished:

1. **Compound Eligibility Evaluation Bug**: `EligibilityEngine._evaluate_compound()` fails 2 unit tests (`test_compound_and_all_pass`, `test_compound_or_one_passes`) in `pytest`.
2. **Frontend–Backend Contract Alignment**: Five frontend pages (`eligibility`, `changelens`, `lifemap`, `applications`, `assistant`) have endpoint path or JSON shape mismatches against backend routers.
3. **Missing Frontend Pages**: `/about`, `/privacy`, `/terms`, `/forgot-password`, `/auth/auth-code-error`, `/coordinator`, `/notifications`, `/settings`, and `/admin/{schemes,documents,jobs,users}` are linked in the UI without page files yet.
4. **Live Runtime Integration Not Executed**: No live Supabase instance, live OpenAI API key, or running PostgreSQL database was exercised in this static + unit-test audit—behavior of `verify_supabase_token()`, `OpenAIProvider`, and `seed_schemes.py` against live services is documented from source code inspection rather than live integration test runs.
5. **Unwired Background Worker & Storage**: `app/workers/__init__.py` is empty, `documents/upload` does not upload bytes to Supabase Storage, `StudentImpact` has no computation service, `assistant/chat` has no vector RAG retrieval, and `Alembic` `versions/` is empty with stale `env.py` imports.
6. **Frontend Unit/E2E Tests**: `jest` and `@playwright/test` are installed in `frontend/package.json` without test files; `npm run lint` fails with 9 errors and 18 warnings.

---

## Related Documentation

- [Documentation Hub](README.md)
- [Project Audit](PROJECT_AUDIT.md)
- [Test Results](08-testing-and-quality/TEST_RESULTS.md)
- [Known Limitations](08-testing-and-quality/KNOWN_LIMITATIONS.md)
