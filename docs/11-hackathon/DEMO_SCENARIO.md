# Demo Scenario

## Short Explanation

This step-by-step walkthrough uses **synthetic student profiles** and **illustrative policy changes** alongside the 4 seeded schemes from `backend/scripts/seed_schemes.py` so presenters can demonstrate NiyamDrishti cleanly without exposing any real student data.

> [!NOTE]
> All student personas and policy revision scenarios below are **synthetic demonstration data**. Verify live backend/frontend contract alignment before running interactive clicks against `POST /api/v1/policy-comparisons` or `/eligibility` (see [Project Audit](../PROJECT_AUDIT.md)).

---

## 1. Synthetic Student Persona (Demo Data)

- **Name**: *Ananya Reddy* (synthetic)
- **State / Domicile**: `Andhra Pradesh`
- **Education**: `ug` (`B.Tech`)
- **Marks Percentage**: `74.0%`
- **Caste Category**: `SC`
- **Annual Family Income**: `₹2,75,000` (`275000` INR)

---

## 2. Live Walkthrough Script

### Step 1: Landing & Scheme Discovery (`/`, `/schemes`)
- Open the Next.js landing page (`http://localhost:3000`) and navigate to **Discover Schemes**.
- Filter by **Andhra Pradesh** to locate the seeded scheme: *Post Matric Scholarship for SC Students — Andhra Pradesh* (`₹15,000`, `AP-SW-PMS-SC-2024`).

### Step 2: Deterministic Eligibility Evaluation (`POST /api/v1/eligibility/evaluate`)
- Evaluate *Ananya's* synthetic profile against the seeded v1 rules (`income <= 250000`, `category in ["SC"]`, `domicile == "Andhra Pradesh"`, `marks >= 50%`):
  - `category`: **PASSED** (`SC` in `["SC"]`)
  - `domicile_state`: **PASSED** (`Andhra Pradesh`)
  - `marks`: **PASSED** (`74.0 >= 50`)
  - `income`: **FAILED** (`275000` does not satisfy `lte 250000`)
  - **Overall Result**: `failed` (`75.0%` match score — 3 of 4 mandatory criteria met)

### Step 3: Illustrative Policy Revision & ChangeLens (`POST /api/v1/policy-comparisons`)
- **Illustrative Demo Revision (v2)**: Suppose a revised notification raises the income ceiling from `250000` to `300000` INR.
- `PolicyComparisonEngine.compare()` detects:
  - `change_type`: `modified`
  - `severity`: `high`
  - `human_summary`: `"Changed 'income' (income): 250000 inr → 300000 inr"`
- Re-running `POST /api/v1/eligibility/evaluate` (or simulation mode `is_simulation: true`) with v2 rules flips *Ananya's* overall result from `failed` to `passed` (`100.0%`).

### Step 4: Reviewer Queue & AI Assistant (`/reviewer`, `/api/docs`)
- Show `/reviewer` displaying extracted rules with confidence badges and `source_text` / `source_page`.
- Show Swagger UI (`http://localhost:8000/api/docs`) for live API inspection (`POST /api/v1/assistant/chat` with `language: "te"` or `"hi"`).

---

## Related Documentation

- [Judge Presentation Guide](JUDGE_PRESENTATION_GUIDE.md)
- [ChangeLens](../02-product/CHANGELENS.md)
- [Eligibility Engine](../02-product/ELIGIBILITY_ENGINE.md)

