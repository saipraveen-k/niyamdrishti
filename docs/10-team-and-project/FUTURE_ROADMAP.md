# Future Roadmap

## Short Explanation

The roadmap prioritizes fixing verified bugs and frontend–backend contract mismatches first, followed by completing the asynchronous document pipeline, RAG citations, impact computation, and production hardening.

---

## 1. Phase-by-Phase Roadmap

### Near-Term (Stabilization & Bug Fixes)
1. **Fix `EligibilityEngine._evaluate_compound()`**: Propagate parent `rule_category` / `rule_key` into sub-conditions so all 35 `pytest` tests pass, and add `contains`/`any` operators.
2. **Align Frontend–Backend API Contracts**: Synchronize routes and JSON fields on `/eligibility`, `/changelens`, `/lifemap`, `/applications`, and `/assistant`.
3. **Resolve ESLint Errors & Missing UI Pages**: Fix the 9 ESLint errors and implement `/about`, `/privacy`, `/terms`, `/forgot-password`, `/notifications`, `/settings`, and `/admin/*` subpages.
4. **Fix Alembic Migrations**: Fix `migrations/env.py` model imports and generate the initial migration revision.

### Medium-Term (Intelligence & Pipeline Completion)
5. **Background Worker & Supabase Storage**: Implement the async job consumer in `app/workers/` and wire `supabase.storage` uploads/downloads.
6. **Automated `StudentImpact` Engine**: Trigger per-student eligibility re-evaluation whenever `POST /api/v1/policy-comparisons` runs.
7. **RAG Vector Retrieval for AI Assistant**: Index approved scheme rules and extracted chunks so `/assistant/chat` returns real page-level `sources`.
8. **Anthropic Provider & Regional OCR**: Implement `AnthropicProvider` and bundle `tesseract-ocr-tel` / `tesseract-ocr-hin` in Docker.

### Long-Term (Scale & Ecosystem)
9. **College Coordinator Portal**: Build `/coordinator` workflows backed by `College` and `CollegeMembership`.
10. **PDF Report Generation & Notifications**: Export ChangeLens and LifeMap PDFs (`generated-reports` bucket) and connect email/SMS alerts.
11. **Redis Caching, Rate Limiting & RLS**: Wire Redis for JWT/scheme caching and rate limits, and commit Supabase SQL RLS policies.

---

## Related Documentation

- [Known Limitations](../08-testing-and-quality/KNOWN_LIMITATIONS.md)
- [Project Milestones](PROJECT_MILESTONES.md)
- [Project Audit](../PROJECT_AUDIT.md)

