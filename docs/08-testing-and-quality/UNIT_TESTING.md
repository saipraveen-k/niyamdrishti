# Unit Testing

## Short Explanation

Backend unit tests verify the two deterministic core engines—`EligibilityEngine` and `PolicyComparisonEngine`—in pure Python with zero database or network calls.

---

## 1. Existing Unit Test Suites

### ChangeLens (`backend/tests/test_comparison_engine.py` — 14 tests)
- **No-change cases**: Identical rules, empty rule lists.
- **Added / Removed / Modified**: Detects added rules (no `old_condition`), removed rules (no `new_condition`), modified conditions, unchanged rules ignored, and note-only changes ignored.
- **Severity & Sorting**: Verifies `income` → `HIGH`, `deadline` → `MEDIUM`, `document` → `LOW`, and `HIGH` sorted before `LOW`.
- **Mixed diff**: Simultaneous add, remove, modify, and unchanged filtering.

### Eligibility Engine (`backend/tests/test_eligibility_engine.py` — 15 tests)
- **Income & Marks**: Passes/fails against thresholds; returns `UNKNOWN` + `missing_fields` when absent.
- **Category (`in` operator)**: Case-insensitive list matching.
- **Multi-rule & Mandatory flag**: All mandatory rules pass vs. one mandatory failure; optional (`is_mandatory=False`) failure does not fail overall result.
- **Compound (`and`/`or`)**: `test_compound_and_all_pass` and `test_compound_or_one_passes` (currently **failing** due to `_evaluate_compound` field mapping bug).
- **Match score & Edge cases**: 50% score calculation, empty rule list (`UNKNOWN`), unsupported operator (`between` → `UNKNOWN`).

---

## 2. Running Unit Tests

```bash
cd backend
pytest tests/test_comparison_engine.py tests/test_eligibility_engine.py -v
```

---

## Related Documentation

- [Test Results](TEST_RESULTS.md)
- [Eligibility Algorithm](../06-ai-and-intelligence/ELIGIBILITY_ALGORITHM.md)
- [Policy Comparison Algorithm](../06-ai-and-intelligence/POLICY_COMPARISON_ALGORITHM.md)

