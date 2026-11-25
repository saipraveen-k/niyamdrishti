# Monitoring

## Short Explanation

NiyamDrishti includes structured JSON/console logging (`structlog`), public and container health check endpoints, and an admin monitoring router—though live DB/job inspection in the monitoring endpoints is still partially stubbed.

---

## 1. Implemented Observability

| Component | Location | What It Provides |
|---|---|---|
| **Structured Logging** | `backend/app/core/logging.py` | `structlog` with ISO timestamps, log level, logger name, contextvars, and `LOG_FORMAT=json\|console` |
| **Public Health Check** | `GET /health` (`app/main.py`) | Returns `status: "ok"`, `app`, `env`, `ai_available` (used by Render & Docker `HEALTHCHECK`) |
| **Admin Health Check** | `GET /api/v1/admin/system-health` (`monitoring/router.py`) | Protected by `admin`/`super_admin`; currently returns static `"ok"`, `"connected"`, `"configured"` strings |
| **Job Monitoring** | `GET /api/v1/admin/jobs` (`monitoring/router.py`) | Stub returning `{"jobs": [], "message": "Job listing requires database query — implement in Phase 9"}` |

---

## 2. Recommended Next Steps for Production Monitoring

1. Update `/api/v1/admin/system-health` to run `SELECT 1` against PostgreSQL and verify Supabase Storage connectivity dynamically.
2. Implement `GET /api/v1/admin/jobs` to query `DocumentProcessingJob` counts by status (`queued`, `processing`, `failed`, `dead`).
3. Connect external uptime alerts (e.g., Render health checks / UptimeRobot) and error tracking (e.g., Sentry) before production traffic.

---

## Related Documentation

- [Backend Architecture](../03-architecture/BACKEND_ARCHITECTURE.md)
- [Admin Workflow](../02-product/ADMIN_WORKFLOW.md)
- [Background Jobs](../03-architecture/BACKGROUND_JOBS.md)

