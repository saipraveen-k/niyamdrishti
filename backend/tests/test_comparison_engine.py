"""
Unit tests for the PolicyComparisonEngine.

Tests are pure Python — no DB or HTTP required.
"""

import pytest
from app.modules.changelens.comparison_engine import (
    PolicyComparisonEngine,
    ChangeType,
    ChangeSeverity,
)


@pytest.fixture
def engine():
    return PolicyComparisonEngine()


# ---------------------------------------------------------------------------
# No changes
# ---------------------------------------------------------------------------


def test_no_changes_when_rules_identical(engine: PolicyComparisonEngine):
    rules = [
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000, "unit": "inr"},
        }
    ]
    changes = engine.compare(rules, rules)
    assert len(changes) == 0


def test_no_changes_for_empty_rules(engine: PolicyComparisonEngine):
    changes = engine.compare([], [])
    assert len(changes) == 0


# ---------------------------------------------------------------------------
# ADDED rules
# ---------------------------------------------------------------------------


def test_added_rule_detected(engine: PolicyComparisonEngine):
    old_rules = []
    new_rules = [
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},
        }
    ]
    changes = engine.compare(old_rules, new_rules)
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.ADDED
    assert changes[0].rule_key == "income"


def test_added_rule_has_no_old_condition(engine: PolicyComparisonEngine):
    old_rules = []
    new_rules = [
        {
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 60},
        }
    ]
    changes = engine.compare(old_rules, new_rules)
    assert changes[0].old_condition is None
    assert changes[0].new_condition is not None


# ---------------------------------------------------------------------------
# REMOVED rules
# ---------------------------------------------------------------------------


def test_removed_rule_detected(engine: PolicyComparisonEngine):
    old_rules = [
        {
            "rule_category": "age",
            "rule_key": "age",
            "condition": {"operator": "lte", "value": 25, "unit": "years"},
        }
    ]
    new_rules = []
    changes = engine.compare(old_rules, new_rules)
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.REMOVED
    assert changes[0].rule_key == "age"


def test_removed_rule_has_no_new_condition(engine: PolicyComparisonEngine):
    old_rules = [
        {
            "rule_category": "age",
            "rule_key": "age",
            "condition": {"operator": "lte", "value": 25},
        }
    ]
    changes = engine.compare(old_rules, [])
    assert changes[0].old_condition is not None
    assert changes[0].new_condition is None


# ---------------------------------------------------------------------------
# MODIFIED rules
# ---------------------------------------------------------------------------


def test_modified_rule_detected(engine: PolicyComparisonEngine):
    old_rules = [
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 250000},
        }
    ]
    new_rules = [
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},  # increased
        }
    ]
    changes = engine.compare(old_rules, new_rules)
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.MODIFIED


def test_unmodified_rule_not_reported(engine: PolicyComparisonEngine):
    rules = [
        {
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 60},
        }
    ]
    changes = engine.compare(rules, rules)
    assert len(changes) == 0


def test_note_change_does_not_trigger_modification(engine: PolicyComparisonEngine):
    """Note-only changes should be ignored (notes are excluded from comparison)."""
    old_rules = [
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000, "note": "old note"},
        }
    ]
    new_rules = [
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000, "note": "new note"},
        }
    ]
    changes = engine.compare(old_rules, new_rules)
    assert len(changes) == 0


# ---------------------------------------------------------------------------
# Severity classification
# ---------------------------------------------------------------------------


def test_income_rule_is_high_severity(engine: PolicyComparisonEngine):
    changes = engine.compare(
        [],
        [
            {
                "rule_category": "income",
                "rule_key": "income",
                "condition": {"operator": "lte", "value": 300000},
            }
        ],
    )
    assert changes[0].severity == ChangeSeverity.HIGH


def test_deadline_rule_is_medium_severity(engine: PolicyComparisonEngine):
    changes = engine.compare(
        [],
        [
            {
                "rule_category": "deadline",
                "rule_key": "deadline",
                "condition": {"operator": "lte", "value": "2024-12-31"},
            }
        ],
    )
    assert changes[0].severity == ChangeSeverity.MEDIUM


def test_document_rule_is_low_severity(engine: PolicyComparisonEngine):
    changes = engine.compare(
        [],
        [
            {
                "rule_category": "document",
                "rule_key": "aadhaar_required",
                "condition": {"operator": "eq", "value": True},
            }
        ],
    )
    assert changes[0].severity == ChangeSeverity.LOW


# ---------------------------------------------------------------------------
# Sorting: HIGH severity first
# ---------------------------------------------------------------------------


def test_changes_sorted_high_before_low(engine: PolicyComparisonEngine):
    old_rules = []
    new_rules = [
        {
            "rule_category": "document",
            "rule_key": "aadhaar",
            "condition": {"operator": "eq", "value": True},
        },
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},
        },
        {
            "rule_category": "deadline",
            "rule_key": "deadline",
            "condition": {"operator": "lte", "value": "2024-12-31"},
        },
    ]
    changes = engine.compare(old_rules, new_rules)
    severities = [c.severity for c in changes]
    assert severities[0] == ChangeSeverity.HIGH
    assert severities[-1] == ChangeSeverity.LOW


# ---------------------------------------------------------------------------
# Mixed: add, remove, modify in one comparison
# ---------------------------------------------------------------------------


def test_mixed_changes(engine: PolicyComparisonEngine):
    old_rules = [
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 250000},
        },
        {
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 60},
        },
        {
            "rule_category": "age",
            "rule_key": "age",
            "condition": {"operator": "lte", "value": 25},
        },
    ]
    new_rules = [
        {
            "rule_category": "income",
            "rule_key": "income",
            "condition": {"operator": "lte", "value": 300000},  # modified
        },
        {
            "rule_category": "marks",
            "rule_key": "marks",
            "condition": {"operator": "gte", "value": 60},  # unchanged
        },
        # age removed
        {
            "rule_category": "disability",
            "rule_key": "is_pwd",
            "condition": {"operator": "eq", "value": False},  # added
        },
    ]
    changes = engine.compare(old_rules, new_rules)
    change_types = {c.change_type for c in changes}
    assert ChangeType.ADDED in change_types
    assert ChangeType.REMOVED in change_types
    assert ChangeType.MODIFIED in change_types
    # Unchanged "marks" should not appear
    assert len(changes) == 3
