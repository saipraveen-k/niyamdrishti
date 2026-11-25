# Objectives and Scope

## Short Explanation

This document defines what NiyamDrishti is built to achieve, what falls inside the current repository scope, and what is explicitly out of scope (such as auto-submitting applications on government portals).

---

## 1. Primary Objectives

1. **Centralized Scheme Discovery**: Provide searchable, filterable access to state (Andhra Pradesh, Telangana) and central/All-India scholarship and fellowship schemes.
2. **Deterministic Eligibility Verification**: Evaluate a student's academic, demographic, and financial profile against approved rules using pure Python comparisons (`lte`, `lt`, `gte`, `gt`, `eq`, `neq`, `in`, `not_in`), never LLM guesswork.
3. **Policy Version Intelligence (ChangeLens)**: Track versioned rule snapshots (`SchemeVersion`) per scheme and compute deterministic diffs (`added`, `removed`, `modified`) with severity ratings (`high`, `medium`, `low`).
4. **Human-in-the-Loop Governance**: Require explicit approval by a `document_reviewer`, `admin`, or `super_admin` before AI-extracted rules affect student evaluations or ChangeLens comparisons.
5. **Actionable Guidance (LifeMap & Tracker)**: Convert eligibility outcomes into structured action plans (`ActionPlan`, `ActionTask`) and manual application tracking (`StudentApplication` + `ApplicationStatusHistory`).
6. **Accessible Multilingual Support**: Support explanations and translation across English (`en`), Telugu (`te`), and Hindi (`hi`).

---

## 2. Scope Matrix

| Area | In Scope (Current Repository) | Out of Scope / Explicit Boundary |
|---|---|---|
| **Geographic Focus** | Andhra Pradesh, Telangana, and All India / Central schemes (4 seeded schemes + admin-added schemes) | International scholarships or non-Indian jurisdictions |
| **Decision Authority** | Automated informational assessments with mandatory disclaimers | Official government eligibility determinations |
| **Application Workflow** | Manual application status tracking (`StudentApplication`) and LifeMap task checklists | Automated submission or scraping/bypassing official government portals |
| **Data Collection** | User-declared academic, income, domicile, and optional category/PwD fields | Collecting Aadhaar numbers, bank account numbers, or payment processing |
| **Authentication** | Supabase Auth (Email/Password + Google OAuth) with backend JWT validation | Custom password hashing in FastAPI or Phone OTP (requires external SMS provider) |
| **Document Formats** | PDF (native + scanned OCR), DOCX, JPEG, PNG, WebP (max 20 MB, 200 pages) | Video/audio policy briefings or arbitrary executable uploads |

---

## 3. Current Scope vs. Implementation Reality

> [!IMPORTANT]
> While all 14 backend modules and primary frontend routes exist in the codebase, background document extraction (`app/workers/`), Supabase Storage binary uploads, automatic `StudentImpact` generation, and RAG vector citations are **partially implemented or planned** and must be completed before full production rollout.

---

## Related Documentation

- [Project Overview](PROJECT_OVERVIEW.md)
- [Target Users](TARGET_USERS.md)
- [Project Audit](../PROJECT_AUDIT.md)
- [Future Roadmap](../10-team-and-project/FUTURE_ROADMAP.md)

