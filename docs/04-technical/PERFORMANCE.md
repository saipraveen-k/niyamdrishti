# Performance

## Short Explanation

NiyamDrishti is engineered for low-latency reads using async SQLAlchemy connection pooling, denormalized scheme summary columns, and deterministic in-memory Python evaluation, while offloading heavy document OCR/AI workloads to a designed job queue.

---

## 1. Implemented Performance Optimizations

| Technique | Location | Benefit |
|---|---|---|
| **Async Database Pooling** | `backend/app/database/database.py` | `asyncpg` with `pool_size=10`, `max_overflow=20`, `pool_pre_ping=True` on PostgreSQL |
| **Denormalized Latest Summary** | `Scheme` (`models/scheme.py`) | `latest_amount`, `latest_deadline`, and `latest_version_id` avoid joining `scheme_versions` on catalog listings |
| **Targeted DB Indexes** | `models/*.py` | Indexes on `schemes(state, is_published, scheme_type)`, `scheme_rules(version_id, rule_category)`, `scheme_documents(sha256_hash)`, `document_processing_jobs(status, scheduled_at)`, `student_scheme_evaluations(student_id, scheme_id)` |
| **SHA-256 Deduplication** | `documents/router.py` | `idempotency_key = f"extract_{sha256}"` prevents duplicate rule-extraction jobs for identical files |
| **Pagination** | `schemes/router.py`, `service.py` | `page` and `per_page` (`1–100`, default `20`) prevent unbounded query responses |
| **Next.js Optimization** | `frontend/next.config.ts` | `cacheComponents: true`, `partialPrefetching: true`, Turbopack CSS bundling |
| **Multi-Worker ASGI** | `backend/Dockerfile`, `render.yaml` | `UVICORN_WORKERS=2` default in production containers |

---

## 2. Current Performance Bottlenecks & Considerations

1. **Per-Request Remote Auth Call**: `verify_supabase_token()` makes an HTTPS round-trip to `{SUPABASE_URL}/auth/v1/user` on every authenticated API request (up to `10s` timeout). Local JWT signature verification or short-lived Redis caching would substantially cut latency.
2. **Unconnected Redis**: `docker-compose.yml` provisions Redis 7, but no caching layer is implemented yet.
3. **Render Free/Starter Cold Starts**: Render Starter instances sleep after inactivity, causing initial cold-start latency.
4. **Synchronous Worker Gap**: OCR (`300 DPI` rendering) and LLM extraction are meant to run in `app/workers/`, which is not yet implemented.

---

## Related Documentation

- [System Architecture](../03-architecture/SYSTEM_ARCHITECTURE.md)
- [Background Jobs](../03-architecture/BACKGROUND_JOBS.md)
- [Deployment Overview](../09-deployment-and-devops/DEPLOYMENT_OVERVIEW.md)

