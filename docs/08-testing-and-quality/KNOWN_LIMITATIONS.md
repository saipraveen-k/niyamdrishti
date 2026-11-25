# Known Limitations

This document describes verified limitations, incomplete wiring, and areas for improvement discovered across the codebase and test runs.

---

## 1. Eligibility Evaluation (`backend/app/modules/eligibility/`)

- ~~**Compound Rules Bug**~~ — **Fixed**: compound `and`/`or` rules now inherit the parent rule's category/key, and `test_compound_and_all_pass` / `test_compound_or_one_passes` pass (all 15 eligibility tests green).
- **Partial Profile Field Mapping**: `_get_profile_field()` covers `income`, `marks`, `cgpa`, `age`, `category`, `disability`, `domicile`, `state`, `course`, and `education_level`. Rules outside these categories return `UNKNOWN`.
- **Unimplemented Operators**: `contains` and `any` appear in `engine.py`'s docstring (and `any` in `RuleOperator`) but are missing from `OPERATOR_MAP`, returning `UNKNOWN`.
- **Directional Match Score**: `match_score` divides `passed_mandatory` by `passed_mandatory + failed_mandatory`—excluding `unknown` mandatory rules from the denominator.

---

## 2. Frontend–Backend Contract & Routing Gaps

- **API Route & Payload Mismatches**:
  - `changelens/page.tsx` calls `GET /changelens/compare/{scheme_id}` (backend exposes `POST /api/v1/policy-comparisons` & `GET /api/v1/policy-comparisons/{comparison_id}`).
  - `lifemap/page.tsx` calls `GET /lifemap/plans` and `PATCH /lifemap/tasks/{taskId}` (backend exposes `GET /api/v1/action-plans/me` and `POST /api/v1/action-plans` with no task patch route).
  - `applications/page.tsx` calls `GET /applications` with `not_started`/`in_progress` statuses (backend exposes `GET /api/v1/applications/me` with `planning`/`documents_gathering`).
  - `assistant/page.tsx` posts `{ session_id, message }` and reads `{ answer, citations }` (backend expects `{ messages, scheme_id, language }` and returns `{ reply, language, sources, disclaimer }`).
  - `eligibility/page.tsx` reads `report.criteria`, uppercase `"PASSED"`, and checks `404` for missing profile (backend returns `criterion_results`, lowercase `"passed"`, and `422` for missing profile).
- **Linked Pages Not Yet Created**: `/about`, `/privacy`, `/terms`, `/forgot-password`, `/auth/auth-code-error`, `/coordinator`, `/notifications`, `/settings`, `/admin/schemes`, `/admin/documents`, `/admin/jobs`, `/admin/users`.
- **ESLint Errors**: `npm run lint` reports 9 errors and 18 warnings (though `tsc --noEmit` passes).

---

## 3. Document Processing, AI & Workers

- **Background Worker Not Implemented**: `backend/app/workers/__init__.py` is empty. `POST /api/v1/documents/upload` queues a `DocumentProcessingJob` in PostgreSQL, but no worker executes `extract_text()` or `OpenAIProvider.extract_structured()`.
- **Supabase Storage Upload Not Wired**: `documents/router.py` constructs `storage_path` without uploading file bytes to Supabase Storage.
- **No RAG Retrieval in AI Assistant**: `assistant/router.py` calls `OpenAIProvider.chat()` directly without vector embeddings or DB document retrieval (`sources` is always `[]`).
- **Anthropic Provider Missing**: `anthropic==0.40.0` and `ANTHROPIC_API_KEY` are configured, but only `OpenAIProvider` is implemented.
- **Regional OCR Language Packs**: `backend/Dockerfile` installs `tesseract-ocr-eng` only; `eng+tel` falls back to `eng` unless `tesseract-ocr-tel` and `tesseract-ocr-hin` are installed.

---

## 4. Database, Migrations & Infrastructure

- **Alembic Migrations**: `versions/` has no migration scripts yet, and `migrations/env.py` imports non-existent classes (`User`, `Application`, `Document`).
- **Unused Redis**: `docker-compose.yml` runs `redis:7-alpine`, but no backend code uses Redis.
- **Stubbed Endpoints**: `GET /api/v1/notifications/me` and `GET /api/v1/admin/jobs` return empty lists; `GET /api/v1/admin/system-health` returns static status values; `StudentImpact` has no computation service yet.
- **No Rate Limiting or Committed RLS SQL**: `LOGIN_MAX_ATTEMPTS` is configured in `Settings` but not enforced; Supabase SQL RLS policies are not in the repo.
- **Scheme Filters**: `max_income` and `min_marks` query parameters in `GET /api/v1/schemes` are accepted by the router but not filtered in `SchemeService.list_schemes()`.
- **Seed Scope**: `scripts/seed_schemes.py` seeds 4 representative schemes (AP, Telangana, and 2 All-India).

---

## Related Documentation

- [Project Audit](../PROJECT_AUDIT.md)
- [Test Results](TEST_RESULTS.md)
- [Future Roadmap](../10-team-and-project/FUTURE_ROADMAP.md)

