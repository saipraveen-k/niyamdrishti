# Project Pitch

## 30-Second Elevator Pitch

> *"Every year, millions of Indian students miss out on scholarships not because they aren't eligible, but because eligibility rules are buried inside 30-page government PDFs that silently change every year. Generic AI chatbots hallucinate those rules. **NiyamDrishti** fixes this: AI extracts structured rules from official notifications into a human-verified database, and pure Python engines deterministically evaluate each student's eligibility and highlight every policy change side-by-side with page-level evidence."*

---

## 1. Pitch Structure (3 Minutes)

1. **The Hook (30s)**: Show a real student's confusion—an income ceiling shifts from ₹2.50 lakh to ₹3.00 lakh in a revised Government Order, or a marks cutoff rises from 50% to 60%. Students either miss out or waste weeks applying when ineligible.
2. **Why Generic AI Isn't Enough (30s)**: If an LLM guesses `passed` or `failed` on a scholarship check, a single hallucination can cost a student ₹20,000–₹70,000 in annual support.
3. **The NiyamDrishti Solution (60s)**:
   - **AI Extracts + Human Approves**: `OpenAIProvider` extracts JSONB rules anchored to verbatim `source_text` and `source_page`; reviewers approve them in `/reviewer`.
   - **Pure Python Decides**: `EligibilityEngine` returns `passed` / `failed` / `unknown` with exact reasons and missing-field hints.
   - **ChangeLens Diffs Versions**: `PolicyComparisonEngine` surfaces `added`, `removed`, and `modified` rules ranked by severity (`high`, `medium`, `low`).
   - **LifeMap & Multilingual Chat**: Converts eligibility into action checklists and supports English, Telugu (`te`), and Hindi (`hi`).
4. **Architecture & Honesty (30s)**: Built on Next.js 16, FastAPI, SQLAlchemy 2.0, and Supabase, with clear separation of completed engines vs. next-phase worker/RAG wiring.
5. **Vision & Impact (30s)**: Expand from the 4 seeded AP/Telangana/All-India schemes to automated GO monitoring across all Indian states and college coordinator portals.

---

## Related Documentation

- [Demo Scenario](DEMO_SCENARIO.md)
- [Expected Impact](EXPECTED_IMPACT.md)
- [Judge Presentation Guide](JUDGE_PRESENTATION_GUIDE.md)

