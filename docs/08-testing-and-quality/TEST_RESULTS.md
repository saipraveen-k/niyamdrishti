# Test Results

## Short Explanation

This page records the **actual observed outputs** of running the repository's test and lint commands on **2026-11-25**—without omitting failures or extrapolating unrun checks.

---

## 1. Backend `pytest -v` Output (`2026-11-25`)

- **Command**: `backend\venv\Scripts\python.exe -m pytest -v` (Python `3.10.11`, pytest `9.2.0`)
- **Summary**: **35 collected — 33 passed, 2 failed** (`0.44s`, exit code `1`)

| Test File | Passed | Failed | Failing Test Names & Observed Cause |
|---|---:|---:|---|
| `tests/test_comparison_engine.py` | 14 | 0 | — |
| `tests/test_eligibility_engine.py` | 13 | 2 | `test_compound_and_all_pass`, `test_compound_or_one_passes` — both returned `EligibilityResult.UNKNOWN` instead of `EligibilityResult.PASSED` because `_evaluate_compound` passes `"other"` / `"sub"` to `_evaluate_rule` instead of the parent `rule_category`/`rule_key` |
| `tests/test_health.py` | 5 | 0 | — |
| `tests/test_sanity.py` | 1 | 0 | — |
| **Total** | **33** | **2** | **2 failures** |

---

## 2. Frontend Checks (`2026-11-25`)

| Check | Command | Outcome | Observed Details |
|---|---|---|---|
| **TypeScript Check** | `cd frontend && npx tsc --noEmit` | **Passed** (`exit 0`) | 0 errors |
| **ESLint** | `cd frontend && npm run lint` | **Failed** (`exit 1`) | 27 problems: **9 errors**, **18 warnings** |
| **Jest / Playwright** | — | **Not run** | No test suites exist in `frontend/` |

---

## Related Documentation

- [Testing Strategy](TESTING_STRATEGY.md)
- [Unit Testing](UNIT_TESTING.md)
- [Frontend Testing](FRONTEND_TESTING.md)
- [Known Limitations](KNOWN_LIMITATIONS.md)

