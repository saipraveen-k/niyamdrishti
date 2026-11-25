# Project Milestones

## Short Explanation

This document tracks NiyamDrishti's completed engineering milestones alongside the remaining integration work identified in the repository audit.

---

## 1. Milestone Timeline

| Milestone | Scope | Observed Status |
|---|---|---|
| **M1 — Foundation & Architecture** | FastAPI app shell, Next.js 16 + Tailwind v4 UI shell, Docker Compose, Render/Vercel configs, GitHub Actions CI | **Completed** |
| **M2 — Database & Auth Layer** | 22 SQLAlchemy 2.0 async models, cross-dialect `JSONB`, Supabase JWT verification, 5-role RBAC, login/register/OAuth callback | **Completed** *(Alembic revisions & auto `user_profiles` sync pending)* |
| **M3 — Core Deterministic Engines** | `EligibilityEngine`, `PolicyComparisonEngine`, `seed_schemes.py` (4 schemes), 35 backend pytest cases | **Completed with 2 known test failures** (compound rules bug) |
| **M4 — AI Extraction & Document Service** | `AIProvider` ABC, `OpenAIProvider`, `ExtractedSchemeRules` schema, magic-byte validation, PyMuPDF + Tesseract OCR + python-docx | **Library Implemented** *(worker loop & Storage upload not wired yet)* |
| **M5 — Student & Reviewer Flows** | Scheme catalog, profile form, eligibility view, ChangeLens UI, reviewer queue, LifeMap, application tracker, AI chat | **UI & Routers Built** *(API contract alignment & missing subpages needed)* |
| **M6 — Full Pipeline Integration & QA** | Fix compound rules, align frontend–backend contracts, wire background worker + Storage + `StudentImpact` + RAG + E2E tests | **Pending / Next Phase** |

---

## Related Documentation

- [Project Audit](../PROJECT_AUDIT.md)
- [Future Roadmap](FUTURE_ROADMAP.md)
- [Test Results](../08-testing-and-quality/TEST_RESULTS.md)

