# Database Schema

## Short Explanation

NiyamDrishti defines **22 SQLAlchemy ORM tables** across 4 modules in `backend/app/database/models/`. All tables use UUID primary keys (`UUIDMixin`) and timezone-aware `created_at` / `updated_at` timestamps (`TimestampMixin`); `schemes` also includes `deleted_at` (`SoftDeleteMixin`). JSONB columns use `app.database.types.JSONB`, which renders as native `JSONB` on PostgreSQL and `JSON` on SQLite.

---

## 1. Users & Institutions (`models/user.py`)

### `user_profiles` (`UserProfile`)
Mirrors Supabase `auth.users` (`id` == Supabase auth user UUID).

| Column | Type | Constraints / Default | Notes |
|---|---|---|---|
| `id` | `UUID` | PK, not null | Matches `auth.users.id` |
| `full_name` | `String(200)` | not null | |
| `email` | `String(254)` | not null, indexed | |
| `phone` | `String(20)` | nullable | |
| `app_role` | `String(50)` | not null, default `"student"` | `student\|college_coordinator\|document_reviewer\|admin\|super_admin` (indexed) |
| `is_active` | `Boolean` | not null, default `True` | |
| `is_verified` | `Boolean` | not null, default `False` | |
| `avatar_url` | `String(500)` | nullable | |
| `preferred_language` | `String(10)` | not null, default `"en"` | |
| `last_login_at` | `DateTime(tz)` | nullable | |
| `created_at`, `updated_at` | `DateTime(tz)` | not null, server `now()` | From `TimestampMixin` |

### `student_profiles` (`StudentProfile`)
1-to-1 eligibility details linked to `user_profiles`.

| Column | Type | Constraints / Default | Notes |
|---|---|---|---|
| `id` | `UUID` | PK | From `UUIDMixin` |
| `user_id` | `UUID` | FK → `user_profiles.id` (`CASCADE`), unique, indexed | |
| `date_of_birth` | `DateTime(tz)` | nullable | Used to calculate `age_years` |
| `gender` | `String(20)` | nullable | |
| `state` | `String(100)` | nullable | |
| `district` | `String(100)` | nullable | |
| `caste_category` | `String(20)` | nullable | `GEN\|OBC\|SC\|ST\|EWS` (user-declared) |
| `is_pwd` | `Boolean` | nullable | Person with disability (user-declared) |
| `pwd_type` | `String(100)` | nullable | |
| `education_level` | `String(50)` | nullable | `10th\|12th\|ug\|pg\|phd` |
| `course_name` | `String(200)` | nullable | |
| `college_name` | `String(300)` | nullable | |
| `college_id` | `UUID` | FK → `colleges.id` (`SET NULL`), nullable | |
| `current_year_semester` | `String(50)` | nullable | |
| `marks_percentage` | `Float` | nullable | |
| `cgpa` | `Float` | nullable | |
| `annual_family_income` | `Integer` | nullable | INR (user-declared) |
| `domicile_state` | `String(100)` | nullable | |
| `domicile_years` | `Integer` | nullable | |
| `profile_completeness` | `Integer` | not null, default `0` | |

### `colleges` (`College`), `college_memberships` (`CollegeMembership`), `admin_invitations` (`AdminInvitation`)

- **`colleges`**: `id`, `name` (`String(300)`), `code` (`String(50)`, unique), `state` (`String(100)`, indexed), `district`, `affiliation`, `is_active`.
- **`college_memberships`**: `id`, `user_id` (FK → `user_profiles.id`), `college_id` (FK → `colleges.id`), `assigned_by` (`UUID`), unique `uq_college_membership(user_id, college_id)`.
- **`admin_invitations`**: `id`, `email`, `invited_role`, `token_hash` (unique `String(64)`), `invited_by`, `expires_at`, `accepted_at`, `is_accepted`.

---

## 2. Schemes, Rules & ChangeLens (`models/scheme.py`)

### `schemes` (`Scheme`)
Includes `UUIDMixin`, `TimestampMixin`, `SoftDeleteMixin` (`deleted_at`).

| Column | Type | Notes |
|---|---|---|
| `id` | `UUID` | PK |
| `name`, `slug` | `String(400)` | `slug` is unique |
| `description` | `Text` | nullable |
| `department`, `scheme_identifier` | `String(300)` / `String(100)` | nullable |
| `state`, `district` | `String(100)` | `state` indexed (`Andhra Pradesh\|Telangana\|Central\|All India`) |
| `education_levels`, `eligible_categories` | `JSONB` | Lists (e.g. `["ug", "pg"]`, `["SC", "ST"]`) |
| `scheme_type` | `String(50)` | default `"scholarship"`, indexed |
| `is_active`, `is_published` | `Boolean` | `is_published` indexed |
| `official_url`, `application_url` | `String(1000)` | nullable |
| `latest_amount`, `latest_deadline`, `latest_version_id` | `Numeric(12,2)`, `DateTime(tz)`, `UUID` | Denormalized summary |

### `scheme_sources` (`SchemeSource`) & `scheme_documents` (`SchemeDocument`)

- **`scheme_sources`**: `id`, `scheme_id` (FK → `schemes.id`), `source_type` (`notification|circular|gazette|website`), `source_url`, `source_title`, `source_date`, `is_verified`, `verified_by`.
- **`scheme_documents`**: `id`, `scheme_id` (FK → `schemes.id`, indexed), `uploaded_by`, `original_filename`, `storage_path` (unique), `file_size_bytes`, `mime_type`, `page_count`, `sha256_hash` (indexed), `source_url`, `is_official`.

### `scheme_versions` (`SchemeVersion`) & `scheme_rules` (`SchemeRule`)

- **`scheme_versions`**: `id`, `scheme_id` (FK → `schemes.id`, indexed), `version_number`, `version_label`, `is_active`, `is_approved`, `approved_by`, `approved_at`, `source_document_id` (FK → `scheme_documents.id`, `SET NULL`), `extraction_run_id`. Unique constraint `uq_scheme_version(scheme_id, version_number)`.
- **`scheme_rules`**: `id`, `version_id` (FK → `scheme_versions.id`, indexed), `rule_category` (indexed), `rule_key`, `condition` (`JSONB`), `source_text` (`Text`), `source_page` (`Integer`), `confidence` (`Float`), `is_mandatory` (`Boolean`), `review_status` (`pending|approved|rejected`), `reviewed_by`, `reviewed_at`, `reviewer_note`.

### `policy_comparisons` (`PolicyComparison`) & `policy_change_events` (`PolicyChangeEvent`)

- **`policy_comparisons`**: `id`, `scheme_id` (FK → `schemes.id`), `old_version_id` (FK → `scheme_versions.id`), `new_version_id` (FK → `scheme_versions.id`), `created_by`, `summary` (`JSONB`), `report_storage_path`.
- **`policy_change_events`**: `id`, `comparison_id` (FK → `policy_comparisons.id`, indexed), `change_type` (`added|removed|modified`), `rule_category`, `rule_key`, `old_value` (`JSONB`), `new_value` (`JSONB`), `old_source_text`, `new_source_text`, `old_source_page`, `new_source_page`, `significance` (`high|medium|low`).

---

## 3. Document Uploads & Job Queue (`models/document.py`)

- **`document_uploads`**: `id`, `user_id` (FK → `user_profiles.id`, indexed), `document_type`, `original_filename`, `storage_path` (unique), `file_size_bytes`, `mime_type`, `sha256_hash`, `is_verified`, `expires_at` (indexed).
- **`document_processing_jobs`**: `id`, `document_id` (indexed), `document_type` (`scheme_document|student_upload`), `job_type`, `idempotency_key` (unique), `status` (`queued|processing|completed|failed|dead`), `priority`, `scheduled_at`, `started_at`, `completed_at`, `next_retry_at`, `attempt_count`, `max_attempts`, `result` (`JSONB`), `error_message`, `progress_pct`, `created_by`, `job_metadata` (`JSONB`). Composite index `ix_jobs_status_scheduled(status, scheduled_at)`.
- **`document_processing_attempts`**: `id`, `job_id` (FK → `document_processing_jobs.id`, indexed), `attempt_number`, `started_at`, `completed_at`, `status`, `error_message`, `worker_id`.

---

## 4. Student Evaluations, Impact, LifeMap & Applications (`models/application.py`)

- **`student_scheme_evaluations`**: `id`, `student_id` (FK → `user_profiles.id`), `scheme_id` (FK → `schemes.id`), `version_id` (FK → `scheme_versions.id`), `overall_result`, `match_score`, `criterion_results` (`JSONB`), `unknown_rules` (`JSONB`), `missing_fields` (`JSONB`), `is_latest`. Composite index `ix_evaluations_student_scheme(student_id, scheme_id)`.
- **`saved_schemes`**: `id`, `student_id` (FK → `user_profiles.id`), `scheme_id` (FK → `schemes.id`), unique `uq_saved_scheme(student_id, scheme_id)`.
- **`student_impacts`**: `id`, `student_id` (FK → `user_profiles.id`), `comparison_id` (FK → `policy_comparisons.id`), `scheme_id` (FK → `schemes.id`), `old_eligibility`, `new_eligibility`, `eligibility_changed`, `impact_summary`, `rule_impacts` (`JSONB`), `is_notified`.
- **`action_plans`**: `id`, `student_id` (FK → `user_profiles.id`), `scheme_id` (FK → `schemes.id`), `evaluation_id`, `status` (`active|completed|abandoned`), `report_storage_path`.
- **`action_tasks`**: `id`, `plan_id` (FK → `action_plans.id`), `task_type`, `title`, `description`, `order_index`, `due_date`, `is_completed`, `completed_at`, `task_metadata` (`JSONB`).
- **`student_applications`**: `id`, `student_id` (FK → `user_profiles.id`), `scheme_id` (FK → `schemes.id`), `status` (`planning|documents_gathering|submitted|under_review|approved|rejected|withdrawn`), `applied_at`, `external_application_id`, `notes`.
- **`application_status_history`**: `id`, `application_id` (FK → `student_applications.id`), `old_status`, `new_status`, `changed_by`, `note`.

---

## Related Documentation

- [Entity Relationship](ENTITY_RELATIONSHIP.md)
- [Database Migrations](DATABASE_MIGRATIONS.md)
- [Database Architecture](../03-architecture/DATABASE_ARCHITECTURE.md)

