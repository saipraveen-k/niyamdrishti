"""
Unit tests for the deterministic EligibilityEngine.

Tests are pure Python — no DB or HTTP required.
"""

import pytest
from app.modules.eligibility.engine import (
    EligibilityEngine,
    EligibilityResult,
)


@pytest.fixture
def engine():
    return EligibilityEngine()


# ---------------------------------------------------------------------------
# Single-rule: income
# ---------------------------------------------------------------------------


def test_income_passes_when_below_threshold(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000, "unit": "inr"},
            "is_mandatory": True,
        }
    ]
    profile = {"annual_family_income": 200000}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.PASSED
    assert report.passed_mandatory == 1
    assert report.failed_mandatory == 0


def test_income_fails_when_above_threshold(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000, "unit": "inr"},
            "is_mandatory": True,
        }
    ]
    profile = {"annual_family_income": 500000}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.FAILED
    assert report.failed_mandatory == 1


def test_income_unknown_when_missing_from_profile(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},
            "is_mandatory": True,
        }
    ]
    profile = {}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.UNKNOWN
    assert "annual_family_income" in report.missing_fields


# ---------------------------------------------------------------------------
# Single-rule: marks
# ---------------------------------------------------------------------------


def test_marks_passes(engine: EligibilityEngine):
    rules = [
        {
            "id": "r2",
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 60},
            "is_mandatory": True,
        }
    ]
    profile = {"marks_percentage": 75}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.PASSED


def test_marks_fails(engine: EligibilityEngine):
    rules = [
        {
            "id": "r2",
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 60},
            "is_mandatory": True,
        }
    ]
    profile = {"marks_percentage": 55}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.FAILED


# ---------------------------------------------------------------------------
# Single-rule: category (string "in" operator)
# ---------------------------------------------------------------------------


def test_category_in_list_passes(engine: EligibilityEngine):
    rules = [
        {
            "id": "r3",
            "rule_category": "category",
            "rule_key": "category",
            "condition": {"operator": "in", "value": ["SC", "ST", "OBC"]},
            "is_mandatory": True,
        }
    ]
    profile = {"caste_category": "SC"}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.PASSED


def test_category_not_in_list_fails(engine: EligibilityEngine):
    rules = [
        {
            "id": "r3",
            "rule_category": "category",
            "rule_key": "category",
            "condition": {"operator": "in", "value": ["SC", "ST"]},
            "is_mandatory": True,
        }
    ]
    profile = {"caste_category": "General"}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.FAILED


# ---------------------------------------------------------------------------
# Multiple rules: all must pass
# ---------------------------------------------------------------------------


def test_multiple_mandatory_rules_all_pass(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},
            "is_mandatory": True,
        },
        {
            "id": "r2",
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 60},
            "is_mandatory": True,
        },
    ]
    profile = {"annual_family_income": 200000, "marks_percentage": 70}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.PASSED
    assert report.match_score == 100.0


def test_one_failed_mandatory_fails_overall(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},
            "is_mandatory": True,
        },
        {
            "id": "r2",
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 60},
            "is_mandatory": True,
        },
    ]
    profile = {"annual_family_income": 200000, "marks_percentage": 50}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.FAILED


# ---------------------------------------------------------------------------
# Non-mandatory rules do not affect overall result
# ---------------------------------------------------------------------------


def test_failed_optional_rule_does_not_fail_overall(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},
            "is_mandatory": True,
        },
        {
            "id": "r2",
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 90},  # optional, student fails
            "is_mandatory": False,
        },
    ]
    profile = {"annual_family_income": 200000, "marks_percentage": 70}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.PASSED
    assert report.total_mandatory == 1


# ---------------------------------------------------------------------------
# Compound (AND/OR) conditions
# ---------------------------------------------------------------------------


def test_compound_and_all_pass(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {
                "logic": "and",
                "sub_conditions": [
                    {"operator": "gte", "value": 50000},
                    {"operator": "lte", "value": 300000},
                ],
            },
            "is_mandatory": True,
        }
    ]
    profile = {"annual_family_income": 150000}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.PASSED


def test_compound_or_one_passes(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "category",
            "rule_key": "category",
            "condition": {
                "logic": "or",
                "sub_conditions": [
                    {"operator": "eq", "value": "SC"},
                    {"operator": "eq", "value": "ST"},
                ],
            },
            "is_mandatory": True,
        }
    ]
    profile = {"caste_category": "SC"}
    report = engine.evaluate(rules, profile)
    assert report.overall_result == EligibilityResult.PASSED


# ---------------------------------------------------------------------------
# Match score calculation
# ---------------------------------------------------------------------------


def test_match_score_fifty_percent(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},
            "is_mandatory": True,
        },
        {
            "id": "r2",
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 90},
            "is_mandatory": True,
        },
    ]
    profile = {"annual_family_income": 200000, "marks_percentage": 70}
    report = engine.evaluate(rules, profile)
    # 1 passed, 1 failed mandatory → 50%
    assert report.match_score == 50.0


# ---------------------------------------------------------------------------
# Empty rules
# ---------------------------------------------------------------------------


def test_no_rules_returns_unknown(engine: EligibilityEngine):
    report = engine.evaluate([], {})
    assert report.overall_result == EligibilityResult.UNKNOWN
    assert report.total_mandatory == 0


# ---------------------------------------------------------------------------
# Unsupported operator
# ---------------------------------------------------------------------------


def test_unsupported_operator_returns_unknown_criterion(engine: EligibilityEngine):
    rules = [
        {
            "id": "r1",
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "between", "value": [100000, 300000]},
            "is_mandatory": True,
        }
    ]
    profile = {"annual_family_income": 200000}
    report = engine.evaluate(rules, profile)
    # "between" is not a supported operator
    cr = report.criterion_results[0]
    assert cr.result == EligibilityResult.UNKNOWN
