# Development Guidelines

## Short Explanation

Follow these engineering standards when contributing to NiyamDrishti so deterministic rules, evidence traceability, and type/test checks remain intact.

---

## 1. Core Architectural Rules

1. **Never Put LLMs in Pass/Fail Decisions**: All eligibility checks (`EligibilityEngine`) and policy comparisons (`PolicyComparisonEngine`) must remain pure, deterministic Python.
2. **Preserve Human-in-the-Loop**: Never query unapproved `SchemeRule` rows (`review_status != "approved"`) for student eligibility or ChangeLens comparisons.
3. **Never Commit Secrets**: Keep `.env`, `.env.local`, API keys, and service role keys out of Git (`.gitignore` excludes `.env*` except `.env.example`).
4. **Always Include Disclaimers**: Eligibility and AI outputs must clearly state they are informational, not official government determinations.

---

## 2. Pre-PR Verification Commands

Run these locally before opening a pull request (matching `.github/workflows/ci.yml`):

```bash
# Backend unit tests
cd backend
pytest tests/ -v --tb=short --ignore=tests/integration

# Frontend TypeScript & Build
cd ../frontend
npx tsc --noEmit
npm run lint
npm run build
```

---

## Related Documentation

- [Development Workflow](../10-team-and-project/DEVELOPMENT_WORKFLOW.md)
- [Testing Strategy](../08-testing-and-quality/TESTING_STRATEGY.md)
- [CI/CD Pipeline](../09-deployment-and-devops/CI_CD_PIPELINE.md)

