# Security

## Short Explanation

NiyamDrishti incorporates multiple defensive controls—server-side JWT validation, role checks, file magic-byte verification, SHA-256 hashing, HTTP security headers, and LLM prompt-injection boundaries—while also having several security hardening items left for production readiness.

---

## 1. Implemented Security Controls

| Control | Location | Details |
|---|---|---|
| **Remote JWT Verification** | `backend/app/core/security.py` | Validates Bearer tokens via Supabase `/auth/v1/user` (`10s` timeout) |
| **Server-Side RBAC** | `backend/app/core/security.py` | `require_roles(...)` guards all admin, document-upload, ChangeLens-create, and reviewer routes |
| **Upload Validation** | `backend/app/modules/documents/service.py` | Enforces 20 MB limit (`max_upload_size_bytes`), MIME allowlist, and magic-byte header matching (`%PDF`, `PK\x03\x04`, JPEG, PNG, WebP) |
| **PDF Page Cap** | `backend/app/modules/documents/service.py` | Rejects PDFs exceeding `max_pdf_pages` (200) to prevent resource exhaustion |
| **Prompt Injection Defense** | `backend/app/ai/providers/openai_provider.py`, `assistant/router.py` | Wraps document text in `<document>` tags and instructs LLM to ignore embedded instructions |
| **CORS Restriction** | `backend/app/main.py` | Restricts origins to `settings.cors_origins_list`, explicit methods and headers |
| **Production Docs Hiding** | `backend/app/main.py` | Sets `docs_url`, `redoc_url`, `openapi_url` to `None` when `APP_ENV == "production"` |
| **Non-Root Container** | `backend/Dockerfile` | Creates and switches to non-root `app` user |
| **HTTP Security Headers** | `frontend/vercel.json` | `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` |
| **CI Dependency Audit** | `.github/workflows/ci.yml` | Runs `pip-audit -r requirements.txt` on `main` branch pushes |

---

## 2. Observed Security Gaps (Important for Production)

1. **No Rate Limiting**: `config.py` defines `login_max_attempts = 5` and `login_attempt_window_minutes = 15`, but no rate-limiting middleware is implemented in FastAPI.
2. **Authoritative Role Source**: `security.py` reads `app_role` from Supabase `user_metadata` rather than `app_metadata` or `user_profiles.app_role`.
3. **No Committed Supabase RLS Policies**: Database tables have no SQL RLS policy scripts committed in the repository yet.
4. **LocalStorage JWT**: Frontend `api-client.ts` reads `nd_access_token` from `localStorage` instead of HTTP-only cookies.
5. **Known `pip-audit` Ignore**: `.github/workflows/ci.yml` passes `--ignore-vuln GHSA-wfm5-x5h8-xm93`.

---

## 3. Related Documentation

- [Authentication](AUTHENTICATION.md)
- [Role-Based Access Control](ROLE_BASED_ACCESS_CONTROL.md)
- [Privacy](PRIVACY.md)
- [Security Testing](../08-testing-and-quality/SECURITY_TESTING.md)

