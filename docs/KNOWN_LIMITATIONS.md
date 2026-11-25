# Known Limitations

> [!NOTE]
> This top-level summary is synchronized with the full technical breakdown in [docs/08-testing-and-quality/KNOWN_LIMITATIONS.md](08-testing-and-quality/KNOWN_LIMITATIONS.md) and [docs/PROJECT_AUDIT.md](PROJECT_AUDIT.md).

---

## Eligibility Evaluation

- ~~**Compound Rules Bug**~~ — **Fixed**: compound `and`/`or` rules now inherit the parent rule's category/key, and `test_compound_and_all_pass` / `test_compound_or_one_passes` pass (all 15 eligibility tests green).
- **Partial Profile Field Coverage**: `_get_profile_field()` maps `income`, `marks`, `cgpa`, `age`, `category`, `disability`, `domicile`, `state`, `course`, and `education_level`. Unmapped criteria return `UNKNOWN`.
- **Unimplemented Operators**: `contains` and `any` appear in docstrings/enums but are not implemented in `OPERATOR_MAP`.
- **Directional Match Score**: Excludes `unknown` mandatory rules from the denominator.

## AI Extraction & Assistant

- **Anthropic Provider Missing**: `AI_PROVIDER=anthropic` is configured in `config.py`, but only `OpenAIProvider` is implemented.
- **AI Assistant Is Direct Chat (No RAG Yet)**: `POST /api/v1/assistant/chat` sends chat messages directly to OpenAI without retrieving scheme chunks (`sources` returns `[]`).
- **OCR Language Packs**: `backend/Dockerfile` installs `tesseract-ocr-eng` only (`eng+tel` falls back to `eng`).

## Policy Comparison (ChangeLens)

- **Key Matching**: Rules match strictly by `(rule_category, rule_key)`—renamed keys appear as `REMOVED` + `ADDED`, and equivalent values in different units (`300000 INR` vs. `3 lakh`) appear as `MODIFIED`.

## Infrastructure, Wiring & Frontend

- **Background Workers Not Wired**: `app/workers/__init__.py` is empty; `documents/upload` queues DB jobs without uploading bytes to Supabase Storage or running extraction.
- **Frontend–Backend Contract Mismatches**: Route/schema mismatches exist on `changelens`, `lifemap`, `applications`, `assistant`, and `eligibility` pages; several linked routes (`/about`, `/privacy`, `/terms`, `/coordinator`, `/notifications`, `/admin/*`) do not have page files yet.
- **Alembic Migrations**: `versions/` has no migration scripts yet and `migrations/env.py` has stale model imports.
- **Stubs & Unused Services**: `notifications/me` and `admin/jobs` return empty stubs; `StudentImpact` has no computation service; `redis` in `docker-compose.yml` is unused in Python; no rate-limiting middleware or committed SQL RLS files exist.
