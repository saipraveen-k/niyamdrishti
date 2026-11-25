# Technical Differentiation

## Short Explanation

Why is NiyamDrishti technically stronger than a typical hackathon "ChatGPT wrapper over PDFs"? Because it separates probabilistic extraction from deterministic execution and preserves auditability at every layer.

---

## 1. Comparison Against Common Alternatives

| Dimension | Generic Scholarship Portal | Naive RAG / LLM Chatbot | NiyamDrishti Architecture |
|---|---|---|---|
| **Eligibility Decision** | None (manual PDF reading) | LLM guesses yes/no (hallucination risk) | Pure-Python `EligibilityEngine` over JSONB rules |
| **Missing Data Handling** | Silent failure or wrong assumption | Often assumes defaults | Explicit `UNKNOWN` state + `missing_fields` list |
| **Policy Revisions** | Replaces PDF without diff | Cannot reliably compare two 30-page versions | `PolicyComparisonEngine` indexes `(category, key)` & classifies severity |
| **Human Oversight** | Manual HTML updates | Unchecked model output | Mandatory `review_status == "approved"` gate in `/reviewer` |
| **Security & Uploads** | Basic extension check | Raw prompt concatenation | Magic-byte validation + SHA-256 + `<document>` injection isolation |
| **Testability** | Coupled to live DB | Non-deterministic outputs | Pure-Python unit tests + cross-dialect `JSONB` on SQLite in-memory |

---

## 2. Key Technical Highlights for Engineering Judges

1. **Cross-Dialect `JSONB` Type (`backend/app/database/types.py`)**: Enables the exact same 22 SQLAlchemy models to run on PostgreSQL `JSONB` in production and `sqlite+aiosqlite:///:memory:` in CI/pytest.
2. **Structured Outputs (`OpenAIProvider.extract_structured`)**: Uses Pydantic `ExtractedSchemeRules` directly as `response_format` with `temperature=0`, eliminating brittle regex JSON parsing.
3. **What-If Simulation Mode**: `POST /api/v1/eligibility/evaluate` supports `is_simulation: true` + `profile_overrides` without polluting persisted `student_scheme_evaluations`.

---

## Related Documentation

- [Key Innovations](../01-overview/KEY_INNOVATIONS.md)
- [System Architecture](../03-architecture/SYSTEM_ARCHITECTURE.md)
- [AI Architecture](../03-architecture/AI_ARCHITECTURE.md)

