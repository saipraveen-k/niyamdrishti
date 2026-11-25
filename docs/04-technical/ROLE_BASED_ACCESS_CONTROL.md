# Role-Based Access Control (RBAC)

## Short Explanation

NiyamDrishti enforces five hierarchical application roles across both the Next.js UI and FastAPI endpoints so students, college coordinators, document reviewers, admins, and super admins only access features permitted for their role.

---

## 1. Role Definitions (`backend/app/core/permissions.py`)

```python
class AppRole(str, Enum):
    STUDENT = "student"
    COLLEGE_COORDINATOR = "college_coordinator"
    DOCUMENT_REVIEWER = "document_reviewer"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
```

| Role | Hierarchy (`RoleChecker`) | Role Groups | Intended Capabilities |
|---|---|---|---|
| `student` | 1 | `ALL_ROLES` | Profiles, eligibility checks, saved schemes, LifeMap, applications, AI chat |
| `college_coordinator` | 2 | `COORDINATOR_ROLES`, `ALL_STAFF_ROLES` | Institutional coordination (`College`, `CollegeMembership` models exist; endpoints/UI pending) |
| `document_reviewer` | 3 | `REVIEWER_ROLES`, `ALL_STAFF_ROLES` | Review queue (`GET /reviews/queue`), rule approval (`POST /reviews/{id}/approve`), ChangeLens comparison (`POST /policy-comparisons`) |
| `admin` | 4 | `ADMIN_ROLES`, `REVIEWER_ROLES`, `COORDINATOR_ROLES`, `ALL_STAFF_ROLES` | Scheme CRUD/publish, official document upload, system health, jobs, plus reviewer permissions |
| `super_admin` | 5 | All groups | Full administrative privileges + `/admin/users` (user management endpoints/UI pending) |

---

## 2. Backend & Frontend Enforcement

### Backend (`backend/app/core/security.py`)

- `RoleChecker(allowed_roles)` is a FastAPI dependency invoked via `require_roles(*roles)`.
- Reads `current_user.app_role` (extracted from Supabase `user_metadata.app_role`, defaulting to `"student"`).
- Raises HTTP `403 Forbidden` if `app_role not in self.allowed_roles`.
- Also defines `require_self_or_roles(user_id_param, *roles)` (currently unused by routers).

### Endpoint Permission Matrix

| Endpoint | Permitted Roles |
|---|---|
| `GET /schemes`, `GET /schemes/{id}`, `GET /health`, `GET /` | Public (`get_optional_user` / open; unpublished schemes require `admin`/`super_admin`) |
| `GET /users/me`, `profiles/*`, `POST /eligibility/evaluate`, `POST /schemes/{id}/bookmark`, `GET /documents/{id}/status`, `GET /policy-comparisons/{id}`, `GET /impacts/me`, `action-plans/*`, `applications/*`, `POST /assistant/chat`, `GET /notifications/me` | Any authenticated role (`get_current_user`) |
| `GET /reviews/queue`, `POST /reviews/{rule_id}/approve`, `POST /policy-comparisons` | `document_reviewer`, `admin`, `super_admin` |
| `POST /admin/schemes`, `PATCH /admin/schemes/{id}`, `POST /admin/schemes/{id}/publish`, `POST /documents/upload`, `GET /admin/system-health`, `GET /admin/jobs` | `admin`, `super_admin` |

### Frontend (`frontend/src/middleware.ts` & `sidebar.tsx`)

- `middleware.ts` checks `user.user_metadata?.app_role` for `/admin`, `/reviewer`, and `/coordinator`, redirecting other roles to `/dashboard`.
- `Sidebar` filters navigation items using `item.roles`.

---

## 3. Security Observation on `user_metadata`

> [!WARNING]
> In Supabase Auth, `user_metadata` is editable by the authenticated user unless locked down or moved to `app_metadata`. Reading `app_role` solely from `user_metadata` works for hackathon prototyping, but production deployments should store authoritative roles in `app_metadata` or verify against `user_profiles.app_role` in PostgreSQL.

---

## Related Documentation

- [Authentication](AUTHENTICATION.md)
- [Security](SECURITY.md)
- [Admin Workflow](../02-product/ADMIN_WORKFLOW.md)

