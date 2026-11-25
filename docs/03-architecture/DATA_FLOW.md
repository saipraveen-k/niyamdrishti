# Data Flow

## Short Explanation

This document traces how data moves end-to-end across NiyamDrishti—from student profiles and official scheme documents to deterministic eligibility reports and ChangeLens policy diffs—explicitly noting which stages are live versus pending wiring.

---

## 1. End-to-End Policy & Student Data Flow

```mermaid
flowchart TD
    subgraph Ingestion["1. Policy Ingestion (Partially Wired)"]
        AD["Admin uploads PDF/DOCX/Image"] -->|POST /api/v1/documents/upload| DOCDB[("scheme_documents + document_processing_jobs")]
        DOCDB -.->|Awaiting worker loop| TXT["extract_text() (PyMuPDF + Tesseract)"]
        TXT -.->|Awaiting worker loop| LLM["OpenAIProvider.extract_structured()"]
        LLM -.->|Creates pending rules| SR[("scheme_rules (review_status='pending')")]
    end

    subgraph Governance["2. Human Review & Publishing (Live)"]
        SR -->|GET /api/v1/reviews/queue| REV["Reviewer UI (/reviewer)"]
        REV -->|POST /api/v1/reviews/{id}/approve| SR_APP[("scheme_rules (review_status='approved')")]
        AD -->|POST /api/v1/admin/schemes/{id}/publish| SCH[("schemes (is_published=true)")]
    end

    subgraph StudentEval["3. Student Eligibility & Action (Live Core)"]
        STU["Student saves profile (/settings/profile)"] -->|POST/PATCH /api/v1/profiles| SP[("student_profiles")]
        SP & SR_APP -->|POST /api/v1/eligibility/evaluate| EE["EligibilityEngine (Pure Python)"]
        EE --> EVAL[("student_scheme_evaluations")]
        EVAL --> LM["LifeMap ActionPlan + Application Tracker"]
    end

    subgraph Diff["4. ChangeLens Comparison (Live Backend)"]
        SR_APP -->|POST /api/v1/policy-comparisons| CE["PolicyComparisonEngine (Pure Python)"]
        CE --> PC[("policy_comparisons + policy_change_events")]
        PC -.->|Computation planned| SI[("student_impacts")]
    end
```

---

## 2. Key Data Flows Explained

### Flow A: Seeded Schemes → Live Eligibility Evaluation (Works Today)
1. `python -m scripts.seed_schemes` populates 4 published `Scheme` records, 4 active & approved `SchemeVersion` records, and approved `SchemeRule` rows.
2. A student authenticates via Supabase Auth and saves their `StudentProfile` (`POST /api/v1/profiles`).
3. `POST /api/v1/eligibility/evaluate` loads the active approved `SchemeVersion` + approved `SchemeRule`s, converts `StudentProfile` into a flat dict via `_build_profile_from_student()`, runs `EligibilityEngine.evaluate()`, stores `StudentSchemeEvaluation`, and returns the result.

### Flow B: Scheme Versioning → ChangeLens Diff (Backend Works Today)
1. Two approved `SchemeVersion` records exist for the same `Scheme`.
2. An admin or reviewer calls `POST /api/v1/policy-comparisons` with `scheme_id`, `old_version_id`, and `new_version_id`.
3. `PolicyComparisonEngine.compare()` compares approved rules by `(rule_category, rule_key)` and persists `PolicyComparison` + `PolicyChangeEvent` rows.

### Flow C: Document Upload → Extraction → Review (Worker Pending)
1. Admin calls `POST /api/v1/documents/upload` — file is validated and a `DocumentProcessingJob` is queued in PostgreSQL.
2. Extraction (`service.py` + `OpenAIProvider.extract_structured`) is implemented at the library level, awaiting the background worker loop (`app/workers/`) and Supabase Storage upload call.

---

## 3. Related Documentation

- [System Architecture](SYSTEM_ARCHITECTURE.md)
- [Document Processing](DOCUMENT_PROCESSING.md)
- [Database Schema](../05-database-and-api/DATABASE_SCHEMA.md)

