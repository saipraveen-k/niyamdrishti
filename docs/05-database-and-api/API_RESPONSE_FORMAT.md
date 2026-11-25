# API Response Format

## Short Explanation

NiyamDrishti uses standard FastAPI JSON responses—returning resource objects or typed Pydantic response schemas directly on success, and `{"detail": "..."}` error envelopes on HTTP `4xx`/`5xx` failures.

---

## 1. Success Response Shapes

### List Pagination (`SchemeListResponse`)

Used by `GET /api/v1/schemes`:

```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Post Matric Scholarship for SC Students — Andhra Pradesh",
      "slug": "ap-post-matric-sc-scholarship",
      "state": "Andhra Pradesh",
      "scheme_type": "scholarship",
      "latest_amount": "15000.00",
      "is_active": true,
      "is_published": true,
      "created_at": "2026-11-25T10:00:00Z"
    }
  ],
  "total": 4,
  "page": 1,
  "per_page": 20,
  "has_next": false
}
```

### Eligibility Evaluation (`EligibilityEvaluateResponse`)

Used by `POST /api/v1/eligibility/evaluate`:

```json
{
  "scheme_id": "uuid",
  "scheme_name": "Post Matric Scholarship for SC Students — Andhra Pradesh",
  "overall_result": "passed",
  "match_score": 100.0,
  "criterion_results": [
    {
      "rule_id": "uuid",
      "rule_category": "income",
      "rule_key": "income",
      "result": "passed",
      "is_mandatory": true,
      "student_value": 200000,
      "required_condition": { "operator": "lte", "value": 250000, "unit": "inr" },
      "explanation": "income: 200000 satisfies lte 250000. ",
      "source_page": 2,
      "confidence": 0.97
    }
  ],
  "missing_fields": [],
  "unknown_rules": [],
  "passed_mandatory": 4,
  "failed_mandatory": 0,
  "total_mandatory": 4,
  "is_simulation": false,
  "evaluation_id": "uuid",
  "disclaimer": "This eligibility assessment is based on user-provided profile information..."
}
```

### Policy Comparison (`PolicyComparisonResponse`)

Used by `POST /api/v1/policy-comparisons` and `GET /api/v1/policy-comparisons/{comparison_id}`:

```json
{
  "comparison_id": "uuid",
  "scheme_id": "uuid",
  "old_version_id": "uuid",
  "new_version_id": "uuid",
  "total_changes": 1,
  "high_severity": 1,
  "medium_severity": 0,
  "low_severity": 0,
  "changes": [
    {
      "id": "uuid",
      "change_type": "modified",
      "rule_category": "income",
      "rule_key": "income",
      "old_value": { "operator": "lte", "value": 250000 },
      "new_value": { "operator": "lte", "value": 300000 },
      "significance": "high",
      "human_summary": "Changed 'income' (income): 250000 → 300000"
    }
  ]
}
```

---

## 2. Error Response Format

All FastAPI `HTTPException` responses return:

```json
{
  "detail": "Human-readable error message"
}
```

Pydantic `422` validation failures return FastAPI's standard validation array:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "scheme_id"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

---

## Related Documentation

- [API Reference](API_REFERENCE.md)
- [Error Handling](../04-technical/ERROR_HANDLING.md)

