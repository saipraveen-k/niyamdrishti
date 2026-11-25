# API Testing

## Short Explanation

API tests exercise FastAPI endpoints over HTTP using `httpx.AsyncClient` and `ASGITransport` wired to an in-memory SQLite session via `app.dependency_overrides[get_db]`.

---

## 1. Current API Test Coverage

Currently, `backend/tests/test_health.py` implements **5 HTTP smoke tests** (plus 1 sanity test in `test_sanity.py`):

- `test_root_endpoint`: `GET /` returns `200` with `message == "NiyamDrishti API"`, `docs`, and `health`.
- `test_health_check`: `GET /health` returns `200` with `status == "ok"`, `app == "NiyamDrishti"`, `env`, `ai_available`.
- `test_health_env_is_development`: Confirms test env is `"development"`.
- `test_openapi_schema_accessible`: `GET /api/openapi.json` returns `200` with `openapi` and `paths`.
- `test_unknown_route_returns_404`: `GET /nonexistent-path-xyz` returns `404`.

---

## 2. API Endpoints Not Yet Covered by Automated Tests

> [!NOTE]
> The following domain endpoints do **not** yet have automated API tests in `backend/tests/`:
> - `schemes` CRUD, search, and bookmarking (`/api/v1/schemes*`, `/api/v1/admin/schemes*`)
> - `profiles` & `users` (`/api/v1/profiles*`, `/api/v1/users/me`)
> - `eligibility/evaluate` (`/api/v1/eligibility/evaluate`)
> - `policy-comparisons` (`/api/v1/policy-comparisons*`)
> - `documents/upload` & `reviews/*`
> - `action-plans/*`, `applications/*`, `assistant/chat`, `impacts/me`
> - RBAC `401`/`403` enforcement tests using mocked `verify_supabase_token`

---

## Related Documentation

- [API Reference](../05-database-and-api/API_REFERENCE.md)
- [Test Results](TEST_RESULTS.md)
- [Testing Strategy](TESTING_STRATEGY.md)

