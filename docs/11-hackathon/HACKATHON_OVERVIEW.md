# Hackathon Overview

## Short Explanation

NiyamDrishti is built as a national-level hackathon submission addressing **EdTech / CivicTech / Public Policy Intelligence**: helping students discover government scholarships and understand policy updates without AI hallucinations.

---

## 1. Submission Snapshot

| Attribute | Details |
|---|---|
| **Project Name** | NiyamDrishti (*"Rule Vision"*) |
| **Tagline** | *Understand policy changes. Discover opportunities. Take the right next step.* |
| **Target Domain** | Government Policy Intelligence & Personalized Student Opportunity Platform |
| **Geographic Focus** | Andhra Pradesh, Telangana, and All-India / Central Government Schemes |
| **Core Architecture** | Next.js 16 + FastAPI + Supabase (PostgreSQL 16, Auth, Storage) + OpenAI + Pure-Python Deterministic Engines |
| **Team Size** | 6 members ([Team Overview](../10-team-and-project/TEAM_OVERVIEW.md)) |

---

## 2. What Makes This Submission Evaluation-Ready

1. **Working Deterministic Core**: `EligibilityEngine` and `PolicyComparisonEngine` (ChangeLens) are implemented in pure Python with unit tests (`backend/tests/`).
2. **Honest Engineering Discipline**: Every planned or partially wired module (background workers, Storage upload, RAG vector citations, `StudentImpact` batch computation) is transparently documented in [Project Audit](../PROJECT_AUDIT.md) and [Known Limitations](../08-testing-and-quality/KNOWN_LIMITATIONS.md).
3. **Safety-First AI Design**: Human-in-the-loop review gates (`review_status == "approved"`), `<document>` prompt-injection wrapping, and explicit legal/official-verification disclaimers.

---

## Related Documentation

- [Project Pitch](PROJECT_PITCH.md)
- [Demo Scenario](DEMO_SCENARIO.md)
- [Technical Differentiation](TECHNICAL_DIFFERENTIATION.md)
- [Judge Presentation Guide](JUDGE_PRESENTATION_GUIDE.md)

