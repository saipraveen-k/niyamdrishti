# Privacy

## Short Explanation

NiyamDrishti is designed around data minimization for student applicants: it collects only the academic, domicile, economic, and optional demographic fields required to evaluate scholarship rules, explicitly avoids collecting Aadhaar numbers or bank account details, and supports configurable retention on student document uploads.

---

## 1. Privacy Design Principles in the Codebase

| Principle | Implementation Evidence |
|---|---|
| **No Aadhaar / Bank Details** | `frontend/src/app/settings/profile/page.tsx` explicitly informs users: *"Your profile data is used only for eligibility evaluation. We do not collect Aadhaar numbers or bank details."* (Only an enum comment `aadhaar_masked` exists on `DocumentUpload.document_type`.) |
| **Optional Sensitive Attributes** | `StudentProfile.caste_category` and `is_pwd` are nullable (`models/user.py`); the UI provides `"Prefer not to say"` for caste category. |
| **User-Declared Labels** | Model comments explicitly mark `caste_category`, `is_pwd`, and `annual_family_income` as `"user-declared; not verified"`. |
| **Retention Configuration** | `config.py` defines `student_doc_retention_days: int = 30`, and `DocumentUpload` includes an indexed `expires_at` column. |
| **Private Storage Buckets** | `config.py` and `docs/DEPLOYMENT.md` specify private buckets (`official-documents`, `student-uploads`, `generated-reports`) with `signed_url_expiry: int = 3600`. |
| **Cascade Deletion** | `StudentProfile`, `DocumentUpload`, `StudentSchemeEvaluation`, `SavedScheme`, `StudentImpact`, `ActionPlan`, and `StudentApplication` all specify `ondelete="CASCADE"` on `user_profiles.id`. |

---

## 2. Current Privacy Gaps (Planned Work)

- **Automated Retention Cleanup**: While `DocumentUpload.expires_at` and `STUDENT_DOC_RETENTION_DAYS` exist, there is no scheduled cleanup job yet to purge expired uploads.
- **Account Deletion & Data Export Endpoints**: Self-service user data export and account deletion APIs are not yet implemented in `users/router.py`.
- **Student Upload Endpoint**: `DocumentUpload` model exists, but student-facing document upload endpoints are not yet exposed.

---

## Related Documentation

- [Security](SECURITY.md)
- [Database Schema](../05-database-and-api/DATABASE_SCHEMA.md)
- [Known Limitations](../08-testing-and-quality/KNOWN_LIMITATIONS.md)

