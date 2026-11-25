# Expected Impact

## Short Explanation

By transforming static, frequently amended government notifications into deterministic, personalized, and multilingual guidance, NiyamDrishti targets measurable reductions in missed scholarship opportunities and wasted application effort—without overclaiming unmeasured production metrics.

---

## 1. Qualitative Impact Pillars

| Beneficiary | Current Friction | Expected Platform Impact |
|---|---|---|
| **Students (AP, Telangana, India)** | Hours spent decoding English PDFs; missing eligibility due to unnoticed amendments | Clear `passed` / `failed` / `unknown` breakdown; ChangeLens diffs; LifeMap checklists; Telugu & Hindi assistant explanations |
| **First-Generation & Rural Applicants** | Confusion over caste, domicile, or income ceilings and required certificates | Guided `missing_fields` prompts and non-punitive `UNKNOWN` status |
| **Document Reviewers & Policy Curators** | Manual re-typing of rules from every new Government Order | AI-assisted structured extraction with side-by-side `source_text` & `source_page` verification |
| **College Coordinators (Planned Portal)** | Advising students manually across dozens of changing schemes | Institutional visibility backed by `College` and `CollegeMembership` models |

---

## 2. Responsible & Honest Guardrails

- **Not Official Determinations**: Every evaluation explicitly displays a disclaimer instructing students to confirm with the issuing government portal.
- **No Auto-Submission**: `StudentApplication` tracks manual progress only, respecting official portal authentication and verification rules.
- **Privacy First**: Avoids storing Aadhaar numbers or bank details; caste and PwD fields are optional and marked user-declared.

---

## Related Documentation

- [Problem Statement](../01-overview/PROBLEM_STATEMENT.md)
- [Privacy](../04-technical/PRIVACY.md)
- [Future Roadmap](../10-team-and-project/FUTURE_ROADMAP.md)

