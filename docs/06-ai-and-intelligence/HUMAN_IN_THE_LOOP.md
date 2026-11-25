# Human-in-the-Loop (HITL) Governance

## Short Explanation

NiyamDrishti treats AI extraction as a **drafting assistant**, never an authority. Every AI-extracted rule enters the system in a `"pending"` state and cannot influence eligibility checks or ChangeLens comparisons until a human reviewer approves it.

---

## 1. Enforcement Points in Code

| Enforcement Point | File | Exact Mechanism |
|---|---|---|
| **Default Pending State** | `models/scheme.py` | `SchemeRule.review_status` defaults to `"pending"`; `SchemeVersion.is_approved` defaults to `False` |
| **Eligibility Filter** | `eligibility/router.py` | Queries only `SchemeVersion.is_approved == True, is_active == True` and `SchemeRule.review_status == "approved"` |
| **ChangeLens Filter** | `changelens/router.py` | `_get_rules()` filters strictly on `SchemeRule.review_status == "approved"` |
| **Review Queue API** | `reviews/router.py` | Restricted via `require_roles("document_reviewer", "admin", "super_admin")` |
| **Audit Trail** | `models/scheme.py`, `reviews/router.py` | Records `reviewed_by`, `reviewed_at`, `reviewer_note`, and optional `corrected_condition` |
| **Reviewer UI** | `frontend/src/app/reviewer/page.tsx` | Highlights rules with `confidence >= 0.8` vs. `< 0.8`, shows JSON + `source_text`, and offers **Approve** / **Reject** buttons |

---

## 2. Current HITL Gaps

- `reviewer/page.tsx` does not yet provide an inline JSON editor for `corrected_condition` or an input box for `note` (even though `ReviewDecisionRequest` supports both).
- Approving rules does not yet automatically promote `SchemeVersion.is_approved = True` / `is_active = True` or update `Scheme.latest_version_id`.

---

## Related Documentation

- [Document Review Workflow](../02-product/DOCUMENT_REVIEW_WORKFLOW.md)
- [Rule Extraction](RULE_EXTRACTION.md)
- [Role-Based Access Control](../04-technical/ROLE_BASED_ACCESS_CONTROL.md)

