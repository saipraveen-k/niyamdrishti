# API Reference

## Short Explanation

All endpoints below were verified directly from `backend/app/main.py` and the 14 router modules under `backend/app/modules/`. Domain routes are prefixed with `/api/v1`.

Interactive OpenAPI docs are available at `/api/docs` and `/api/redoc` when `APP_ENV != "production"`.

---

## 1. Root & Health Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/` | Public | Returns `{"message": "NiyamDrishti API", "docs": "/api/docs", "health": "/health"}` |
| `GET` | `/health` | Public | Returns `{"status": "ok", "app": "NiyamDrishti", "env": ..., "ai_available": ...}` |

---

## 2. Authentication, Users & Profiles

| Method | Path | Auth / Role | Request Body / Params | Response / Notes |
|---|---|---|---|---|
| `GET` | `/api/v1/auth/status` | Public | — | Returns `{"status": "auth module active — Supabase Auth handles authentication"}` |
| `GET` | `/api/v1/users/me` | Authenticated | — | Returns `{id, email, app_role, full_name, preferred_language}` from `user_profiles` (`404` if missing) |
| `GET` | `/api/v1/profiles/me` | Authenticated | — | Returns current user's `StudentProfile` (`404` if missing) |
| `POST` | `/api/v1/profiles` | Authenticated | `ProfileUpdateRequest` (`state`, `district`, `education_level`, `course_name`, `college_name`, `marks_percentage`, `cgpa`, `annual_family_income`, `caste_category`, `is_pwd`) | `201 Created`; returns `409` if profile already exists |
| `PATCH` | `/api/v1/profiles/me` | Authenticated | `ProfileUpdateRequest` (partial) | Updates `StudentProfile` (`404` if missing) |

---

## 3. Schemes

| Method | Path | Auth / Role | Request Body / Params | Response / Notes |
|---|---|---|---|---|
| `GET` | `/api/v1/schemes` | Public (`get_optional_user`) | Query: `q`, `state`, `education_level`, `scheme_type`, `category`, `max_income`, `min_marks`, `page`, `per_page` | Returns `SchemeListResponse`. *(Note: `max_income` and `min_marks` are not filtered in `SchemeService` yet.)* |
| `GET` | `/api/v1/schemes/{scheme_id}` | Public (`get_optional_user`) | Path: `scheme_id: UUID` | Returns `SchemeDetail`; unpublished schemes require `admin` or `super_admin` |
| `POST` | `/api/v1/admin/schemes` | `admin`, `super_admin` | `SchemeCreateRequest` | `201 Created` (`SchemeDetail`), initially `is_published=False` |
| `PATCH` | `/api/v1/admin/schemes/{scheme_id}` | `admin`, `super_admin` | `SchemeUpdateRequest` | Updates scheme (`404` if missing) |
| `POST` | `/api/v1/admin/schemes/{scheme_id}/publish` | `admin`, `super_admin` | Path: `scheme_id: UUID` | Sets `is_published=True` (`404` if missing) |
| `POST` | `/api/v1/schemes/{scheme_id}/bookmark` | Authenticated | Path: `scheme_id: UUID` | `204 No Content`; toggles row in `saved_schemes` |

---

## 4. Eligibility Evaluation

| Method | Path | Auth / Role | Request Body / Params | Response / Notes |
|---|---|---|---|---|
| `POST` | `/api/v1/eligibility/evaluate` | Authenticated | `EligibilityEvaluateRequest` (`scheme_id`, `profile_overrides`, `is_simulation`) | Returns `EligibilityEvaluateResponse` (`overall_result`: `"passed"\|"failed"\|"unknown"`, `match_score`, `criterion_results`, `missing_fields`, `unknown_rules`, `disclaimer`). Persists `StudentSchemeEvaluation` unless `is_simulation=true`. |

---

## 5. Documents & Reviews

| Method | Path | Auth / Role | Request Body / Params | Response / Notes |
|---|---|---|---|---|
| `POST` | `/api/v1/documents/upload` | `admin`, `super_admin` | Multipart form: `scheme_id` (UUID), `source_url` (optional), `file` (`UploadFile`) | `201 Created`; validates size/MIME/magic bytes, creates `SchemeDocument` + queued `DocumentProcessingJob`. *(Does not upload bytes to Storage or run extraction yet.)* |
| `GET` | `/api/v1/documents/{document_id}/status` | Authenticated | Path: `document_id: UUID` | Returns `{document_id, status, progress_pct, attempt_count, error_message}` |
| `GET` | `/api/v1/reviews/queue` | `document_reviewer`, `admin`, `super_admin` | — | Lists up to 50 `SchemeRule` rows with `review_status == "pending"` |
| `POST` | `/api/v1/reviews/{rule_id}/approve` | `document_reviewer`, `admin`, `super_admin` | `ReviewDecisionRequest` (`decision`, `note`, `corrected_condition`) | Updates rule review status, reviewer ID, timestamp, and optional corrected JSONB condition |

---

## 6. ChangeLens & Personalized Impact

| Method | Path | Auth / Role | Request Body / Params | Response / Notes |
|---|---|---|---|---|
| `POST` | `/api/v1/policy-comparisons` | `admin`, `super_admin`, `document_reviewer` | `CompareVersionsRequest` (`scheme_id`, `old_version_id`, `new_version_id`) | Compares approved rules via `PolicyComparisonEngine`, persists `PolicyComparison` + `PolicyChangeEvent`, returns `PolicyComparisonResponse` |
| `GET` | `/api/v1/policy-comparisons/{comparison_id}` | Authenticated | Path: `comparison_id: UUID` | Returns saved `PolicyComparisonResponse` |
| `GET` | `/api/v1/impacts/me` | Authenticated | — | Returns up to 20 `StudentImpact` records for current student |

---

## 7. LifeMap, Applications & AI Assistant

| Method | Path | Auth / Role | Request Body / Params | Response / Notes |
|---|---|---|---|---|
| `GET` | `/api/v1/action-plans/me` | Authenticated | — | Lists active `ActionPlan` records (`id`, `scheme_id`, `status`) |
| `POST` | `/api/v1/action-plans` | Authenticated | `CreateActionPlanRequest` (`scheme_id`, `evaluation_id`) | `201 Created`; inserts `ActionPlan` + 3 default `ActionTask` items |
| `GET` | `/api/v1/applications/me` | Authenticated | — | Lists user's `StudentApplication` records (`id`, `scheme_id`, `status`) |
| `POST` | `/api/v1/applications` | Authenticated | `CreateApplicationRequest` (`scheme_id`) | `201 Created` with `status: "planning"` |
| `PATCH` | `/api/v1/applications/{application_id}` | Authenticated | `UpdateApplicationRequest` (`status`, `notes`) | Updates status and appends `ApplicationStatusHistory` row |
| `POST` | `/api/v1/assistant/chat` | Authenticated | `ChatRequest` (`messages: [{role, content}]`, `scheme_id`, `language`) | Calls `OpenAIProvider.chat` (`en\|te\|hi`); returns `ChatResponse` (`reply`, `language`, `sources`, `disclaimer`) |

---

## 8. Notifications & Admin Monitoring

| Method | Path | Auth / Role | Status |
|---|---|---|---|
| `GET` | `/api/v1/notifications/me` | Authenticated | **Stub**: returns `{"notifications": [], "unread_count": 0}` |
| `GET` | `/api/v1/admin/system-health` | `admin`, `super_admin` | Returns static `{"status": "ok", "database": "connected", "ai": "configured", "storage": "configured"}` |
| `GET` | `/api/v1/admin/jobs` | `admin`, `super_admin` | **Stub**: returns `{"jobs": [], "message": "Job listing requires database query — implement in Phase 9"}` |

---

## Related Documentation

- [API Response Format](API_RESPONSE_FORMAT.md)
- [API Architecture](../03-architecture/API_ARCHITECTURE.md)
- [Project Audit](../PROJECT_AUDIT.md)

