# Judge Presentation Guide

## Short Explanation

This guide prepares the team for technical Q&A with hackathon judges, ensuring crisp, truthful answers backed directly by files in the repository.

---

## 1. Anticipated Judge Questions & Evidence-Backed Answers

### Q1: "How do you prevent AI hallucinations in eligibility decisions?"
- **Answer**: Generative AI is **never** called during eligibility evaluation or policy comparison. `OpenAIProvider.extract_structured()` only parses documents into Pydantic-validated JSONB rules (`review_status="pending"`), a human reviewer approves them in `/reviewer`, and pure Python (`EligibilityEngine` in `backend/app/modules/eligibility/engine.py` and `PolicyComparisonEngine` in `backend/app/modules/changelens/comparison_engine.py`) executes all comparisons deterministically.

### Q2: "What is working today vs. what is still in progress?"
- **Answer** *(honest & transparent)*:
  - **Working & tested**: Core FastAPI app, 22-table SQLAlchemy schema, Supabase Auth JWT + RBAC middleware, `PolicyComparisonEngine` (14/14 unit tests pass), `EligibilityEngine` single-rule & score logic (13/15 pass; we identified a compound-rule key-propagation bug in `_evaluate_compound` affecting 2 tests), seed script for 4 AP/Telangana/Central schemes, and Next.js 16 frontend (`tsc --noEmit` passes).
  - **In progress / next phase**: Wiring `app/workers/` to execute queued document extraction jobs, uploading document bytes to Supabase Storage, automating `StudentImpact` generation on policy comparisons, connecting vector RAG retrieval for assistant citations, and aligning 5 frontend–backend endpoint contracts.

### Q3: "How do you handle privacy for sensitive student data like caste or income?"
- **Answer**: We collect only fields directly tied to scholarship rules (`StudentProfile`), make `caste_category` and `is_pwd` optional (`"Prefer not to say"`), explicitly avoid Aadhaar numbers and bank details, configure 30-day retention (`STUDENT_DOC_RETENTION_DAYS`), and define cascade deletes on `user_profiles.id`.

### Q4: "How do you defend against malicious uploads or prompt injection in policy PDFs?"
- **Answer**: `validate_upload()` (`documents/service.py`) checks file size (`<= 20 MB`), MIME allowlist, and binary magic bytes (`%PDF`, `PK\x03\x04`, JPEG, PNG, WebP), and caps PDFs at 200 pages. `OpenAIProvider.extract_structured()` wraps extracted text in `<document>` tags with explicit system instructions to ignore any directive text inside documents.

---

## 2. Live Demo Checklist (Before Going on Stage)

1. Start PostgreSQL (or Supabase) and run `python -m scripts.seed_schemes` in `backend/`.
2. Start backend (`uvicorn app.main:app --reload`) and verify `http://localhost:8000/health` and `/api/docs`.
3. Start frontend (`npm run dev`) and verify `http://localhost:3000`.
4. Keep `pytest -v` output and [Architecture Diagram](../diagrams/system-architecture.mmd) ready for technical deep-dives.

---

## Related Documentation

- [Hackathon Overview](HACKATHON_OVERVIEW.md)
- [Demo Scenario](DEMO_SCENARIO.md)
- [Project Audit](../PROJECT_AUDIT.md)

