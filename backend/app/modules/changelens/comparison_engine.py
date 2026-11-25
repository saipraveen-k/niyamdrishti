"""
ChangeLens — Policy Version Comparison Engine.

Deterministic Python comparison of two approved scheme rule sets.
The LLM extracts rules; this module calculates differences.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ChangeType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


class ChangeSeverity(str, Enum):
    HIGH = "high"    # Eligibility threshold changes
    MEDIUM = "medium"  # Amount, deadline changes
    LOW = "low"       # Administrative, procedural changes


@dataclass
class RuleChange:
    change_type: ChangeType
    rule_category: str
    rule_key: str
    old_condition: Optional[Dict[str, Any]]
    new_condition: Optional[Dict[str, Any]]
    old_source_text: Optional[str]
    new_source_text: Optional[str]
    old_source_page: Optional[int]
    new_source_page: Optional[int]
    severity: ChangeSeverity
    human_summary: str


class PolicyComparisonEngine:
    """
    Compares two sets of approved scheme rules.
    Returns a structured list of change events.
    """

    HIGH_SEVERITY_CATEGORIES = {
        "income", "marks", "cgpa", "age", "category",
        "disability", "domicile", "state", "exclusion",
    }
    MEDIUM_SEVERITY_CATEGORIES = {"amount", "deadline"}

    def compare(
        self,
        old_rules: List[Dict[str, Any]],
        new_rules: List[Dict[str, Any]],
    ) -> List[RuleChange]:
        """
        Compare old and new rule lists.
        Rules are matched by rule_key within the same rule_category.
        """
        changes: List[RuleChange] = []

        # Index rules by (category, key)
        old_index: Dict[Tuple[str, str], Dict] = {
            (r["rule_category"], r["rule_key"]): r for r in old_rules
        }
        new_index: Dict[Tuple[str, str], Dict] = {
            (r["rule_category"], r["rule_key"]): r for r in new_rules
        }

        old_keys = set(old_index.keys())
        new_keys = set(new_index.keys())

        # Removed rules
        for key in old_keys - new_keys:
            old_rule = old_index[key]
            changes.append(
                RuleChange(
                    change_type=ChangeType.REMOVED,
                    rule_category=key[0],
                    rule_key=key[1],
                    old_condition=old_rule.get("condition"),
                    new_condition=None,
                    old_source_text=old_rule.get("source_text"),
                    new_source_text=None,
                    old_source_page=old_rule.get("source_page"),
                    new_source_page=None,
                    severity=self._severity(key[0]),
                    human_summary=self._summary_removed(key[0], key[1], old_rule),
                )
            )

        # Added rules
        for key in new_keys - old_keys:
            new_rule = new_index[key]
            changes.append(
                RuleChange(
                    change_type=ChangeType.ADDED,
                    rule_category=key[0],
                    rule_key=key[1],
                    old_condition=None,
                    new_condition=new_rule.get("condition"),
                    old_source_text=None,
                    new_source_text=new_rule.get("source_text"),
                    old_source_page=None,
                    new_source_page=new_rule.get("source_page"),
                    severity=self._severity(key[0]),
                    human_summary=self._summary_added(key[0], key[1], new_rule),
                )
            )

        # Modified rules
        for key in old_keys & new_keys:
            old_rule = old_index[key]
            new_rule = new_index[key]
            if self._conditions_differ(old_rule.get("condition"), new_rule.get("condition")):
                changes.append(
                    RuleChange(
                        change_type=ChangeType.MODIFIED,
                        rule_category=key[0],
                        rule_key=key[1],
                        old_condition=old_rule.get("condition"),
                        new_condition=new_rule.get("condition"),
                        old_source_text=old_rule.get("source_text"),
                        new_source_text=new_rule.get("source_text"),
                        old_source_page=old_rule.get("source_page"),
                        new_source_page=new_rule.get("source_page"),
                        severity=self._severity(key[0]),
                        human_summary=self._summary_modified(key[0], key[1], old_rule, new_rule),
                    )
                )

        # Sort by severity: HIGH first
        severity_order = {
            ChangeSeverity.HIGH: 0,
            ChangeSeverity.MEDIUM: 1,
            ChangeSeverity.LOW: 2,
        }
        changes.sort(key=lambda c: severity_order[c.severity])

        return changes

    def _conditions_differ(
        self, old: Optional[dict], new: Optional[dict]
    ) -> bool:
        if old is None and new is None:
            return False
        if old is None or new is None:
            return True
        # Normalize for comparison
        return self._normalize_condition(old) != self._normalize_condition(new)

    def _normalize_condition(self, condition: dict) -> dict:
        """Create a comparable normalized form."""
        if not condition:
            return {}
        # Convert values to strings for consistent comparison
        result = {}
        for k, v in condition.items():
            if k == "note":
                continue  # Ignore note changes
            if isinstance(v, (int, float)):
                result[k] = str(v)
            elif isinstance(v, list):
                result[k] = sorted([str(x) for x in v])
            else:
                result[k] = str(v).lower().strip() if v is not None else None
        return result

    def _severity(self, category: str) -> ChangeSeverity:
        if category in self.HIGH_SEVERITY_CATEGORIES:
            return ChangeSeverity.HIGH
        if category in self.MEDIUM_SEVERITY_CATEGORIES:
            return ChangeSeverity.MEDIUM
        return ChangeSeverity.LOW

    def _summary_removed(self, category: str, key: str, rule: dict) -> str:
        cond = rule.get("condition", {})
        val = cond.get("value")
        unit = cond.get("unit", "")
        return (
            f"Requirement removed: '{key}' ({category})"
            + (f" [was: {cond.get('operator')} {val}{' ' + unit if unit else ''}]" if val else "")
        )

    def _summary_added(self, category: str, key: str, rule: dict) -> str:
        cond = rule.get("condition", {})
        val = cond.get("value")
        unit = cond.get("unit", "")
        return (
            f"New requirement added: '{key}' ({category})"
            + (f" [{cond.get('operator')} {val}{' ' + unit if unit else ''}]" if val else "")
        )

    def _summary_modified(self, category: str, key: str, old: dict, new: dict) -> str:
        old_cond = old.get("condition", {})
        new_cond = new.get("condition", {})
        old_val = old_cond.get("value")
        new_val = new_cond.get("value")
        unit = new_cond.get("unit") or old_cond.get("unit") or ""

        if old_val is not None and new_val is not None and old_val != new_val:
            return (
                f"Changed '{key}' ({category}): "
                f"{old_val}{' ' + unit if unit else ''} → {new_val}{' ' + unit if unit else ''}"
            )
        return f"Modified '{key}' ({category})"


comparison_engine = PolicyComparisonEngine()
