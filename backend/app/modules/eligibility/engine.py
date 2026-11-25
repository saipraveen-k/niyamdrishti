"""
Deterministic eligibility evaluation engine.

The LLM extracts and structures rules. This module evaluates them
against a student profile using Python arithmetic. No AI guessing.

Rule condition schema (JSONB in DB):
{
  "operator": "lte" | "gte" | "lt" | "gt" | "eq" | "neq" | "in" | "not_in" | "contains" | "any",
  "value": <scalar or list>,
  "unit": "inr" | "percent" | "cgpa" | "years" | null,
  "logic": "and" | "or" | null,
  "sub_conditions": [...],  # for compound rules
  "note": "explanation string"
}
"""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class EligibilityResult(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    UNKNOWN = "unknown"
    NEEDS_VERIFICATION = "needs_verification"


@dataclass
class CriterionResult:
    rule_id: str
    rule_category: str
    rule_key: str
    result: EligibilityResult
    is_mandatory: bool
    student_value: Optional[Any]
    required_condition: dict
    explanation: str
    source_page: Optional[int] = None
    confidence: Optional[float] = None


@dataclass
class EvaluationReport:
    overall_result: EligibilityResult
    match_score: float
    criterion_results: List[CriterionResult] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    unknown_rules: List[str] = field(default_factory=list)
    passed_mandatory: int = 0
    failed_mandatory: int = 0
    total_mandatory: int = 0


class EligibilityEngine:
    """
    Evaluates a student profile against a list of scheme rules.
    All evaluation is deterministic Python — no AI involvement.
    """

    OPERATOR_MAP = {
        "lte": lambda a, b: float(a) <= float(b),
        "lt": lambda a, b: float(a) < float(b),
        "gte": lambda a, b: float(a) >= float(b),
        "gt": lambda a, b: float(a) > float(b),
        "eq": lambda a, b: str(a).lower() == str(b).lower(),
        "neq": lambda a, b: str(a).lower() != str(b).lower(),
        "in": lambda a, b: str(a).lower() in [str(x).lower() for x in b],
        "not_in": lambda a, b: str(a).lower() not in [str(x).lower() for x in b],
    }

    def evaluate(
        self,
        rules: List[dict],
        student_profile: Dict[str, Any],
    ) -> EvaluationReport:
        """
        Main evaluation entry point.

        Args:
            rules: List of rule dicts from SchemeRule.condition
            student_profile: Flattened dict of student profile fields

        Returns:
            EvaluationReport with per-criterion and overall results
        """
        criterion_results: List[CriterionResult] = []
        missing_fields: List[str] = []
        unknown_rule_keys: List[str] = []

        for rule in rules:
            result = self._evaluate_rule(rule, student_profile, missing_fields)
            criterion_results.append(result)
            if result.result == EligibilityResult.UNKNOWN:
                unknown_rule_keys.append(rule.get("rule_key", "unknown"))

        # Aggregate
        mandatory_results = [r for r in criterion_results if r.is_mandatory]
        total_mandatory = len(mandatory_results)
        passed_mandatory = sum(1 for r in mandatory_results if r.result == EligibilityResult.PASSED)
        failed_mandatory = sum(1 for r in mandatory_results if r.result == EligibilityResult.FAILED)
        unknown_mandatory = sum(1 for r in mandatory_results if r.result == EligibilityResult.UNKNOWN)

        # Overall result logic
        if failed_mandatory > 0:
            overall = EligibilityResult.FAILED
        elif unknown_mandatory > 0:
            overall = EligibilityResult.UNKNOWN
        elif passed_mandatory == total_mandatory and total_mandatory > 0:
            overall = EligibilityResult.PASSED
        else:
            overall = EligibilityResult.UNKNOWN

        # Match score: passed / (passed + failed) for mandatory rules only
        # Does NOT imply official eligibility
        evaluated_mandatory = passed_mandatory + failed_mandatory
        if evaluated_mandatory > 0:
            match_score = round((passed_mandatory / evaluated_mandatory) * 100, 1)
        else:
            match_score = 0.0

        return EvaluationReport(
            overall_result=overall,
            match_score=match_score,
            criterion_results=criterion_results,
            missing_fields=list(set(missing_fields)),
            unknown_rules=unknown_rule_keys,
            passed_mandatory=passed_mandatory,
            failed_mandatory=failed_mandatory,
            total_mandatory=total_mandatory,
        )

    def _evaluate_rule(
        self,
        rule: dict,
        profile: Dict[str, Any],
        missing_fields: List[str],
    ) -> CriterionResult:
        rule_id = rule.get("id", "")
        rule_category = rule.get("rule_category", "other")
        rule_key = rule.get("rule_key", "")
        condition = rule.get("condition", {})
        is_mandatory = rule.get("is_mandatory", True)
        source_page = rule.get("source_page")
        confidence = rule.get("confidence")

        # Determine which profile field to use
        profile_field = self._get_profile_field(rule_category, rule_key)

        if profile_field and profile_field not in profile:
            missing_fields.append(profile_field)
            return CriterionResult(
                rule_id=rule_id,
                rule_category=rule_category,
                rule_key=rule_key,
                result=EligibilityResult.UNKNOWN,
                is_mandatory=is_mandatory,
                student_value=None,
                required_condition=condition,
                explanation=f"Profile field '{profile_field}' not provided",
                source_page=source_page,
                confidence=confidence,
            )

        student_value = profile.get(profile_field) if profile_field else None

        # Handle compound conditions
        if condition.get("logic") in ("and", "or"):
            result, explanation = self._evaluate_compound(
                condition, profile, missing_fields, rule_category, rule_key
            )
        elif student_value is None:
            result = EligibilityResult.UNKNOWN
            explanation = f"Cannot evaluate '{rule_key}': missing profile data"
        else:
            result, explanation = self._apply_operator(
                student_value, condition, rule_key
            )

        return CriterionResult(
            rule_id=rule_id,
            rule_category=rule_category,
            rule_key=rule_key,
            result=result,
            is_mandatory=is_mandatory,
            student_value=student_value,
            required_condition=condition,
            explanation=explanation,
            source_page=source_page,
            confidence=confidence,
        )

    def _apply_operator(
        self, student_value: Any, condition: dict, rule_key: str
    ) -> tuple[EligibilityResult, str]:
        operator = condition.get("operator")
        required_value = condition.get("value")
        unit = condition.get("unit", "")
        note = condition.get("note", "")

        if not operator or required_value is None:
            return (
                EligibilityResult.UNKNOWN,
                f"Incomplete rule condition for '{rule_key}'",
            )

        op_fn = self.OPERATOR_MAP.get(operator)
        if not op_fn:
            return (
                EligibilityResult.UNKNOWN,
                f"Unsupported operator '{operator}' for '{rule_key}'",
            )

        try:
            passed = op_fn(student_value, required_value)
        except (TypeError, ValueError) as e:
            return (
                EligibilityResult.UNKNOWN,
                f"Could not compare '{student_value}' with '{required_value}': {e}",
            )

        unit_str = f" {unit}" if unit else ""
        if passed:
            return (
                EligibilityResult.PASSED,
                f"{rule_key}: {student_value}{unit_str} satisfies {operator} {required_value}{unit_str}. {note}",
            )
        else:
            return (
                EligibilityResult.FAILED,
                f"{rule_key}: {student_value}{unit_str} does not satisfy {operator} {required_value}{unit_str}. {note}",
            )

    def _evaluate_compound(
        self,
        condition: dict,
        profile: Dict[str, Any],
        missing_fields: List[str],
        parent_category: str = "other",
        parent_key: str = "",
    ) -> tuple[EligibilityResult, str]:
        logic = condition.get("logic", "and")
        sub_conditions = condition.get("sub_conditions", [])

        if not sub_conditions:
            return EligibilityResult.UNKNOWN, "Empty compound condition"

        sub_results = []
        for sub in sub_conditions:
            # Sub-conditions inherit the parent rule's category/key (and therefore
            # its profile field) unless they name their own, e.g. a compound rule
            # mixing income and marks.
            temp_rule = {
                "rule_category": sub.get("rule_category", parent_category),
                "rule_key": sub.get("rule_key", parent_key),
                "condition": sub,
                "is_mandatory": True,
            }
            cr = self._evaluate_rule(temp_rule, profile, missing_fields)
            sub_results.append(cr)

        if logic == "or":
            if any(r.result == EligibilityResult.PASSED for r in sub_results):
                return EligibilityResult.PASSED, "One or more conditions satisfied (OR)"
            elif any(r.result == EligibilityResult.UNKNOWN for r in sub_results):
                return EligibilityResult.UNKNOWN, "Some conditions could not be evaluated (OR)"
            else:
                return EligibilityResult.FAILED, "No conditions satisfied (OR)"
        else:  # and
            if all(r.result == EligibilityResult.PASSED for r in sub_results):
                return EligibilityResult.PASSED, "All conditions satisfied (AND)"
            elif any(r.result == EligibilityResult.FAILED for r in sub_results):
                return EligibilityResult.FAILED, "One or more conditions failed (AND)"
            else:
                return EligibilityResult.UNKNOWN, "Some conditions could not be evaluated (AND)"

    def _get_profile_field(self, rule_category: str, rule_key: str) -> Optional[str]:
        """Map rule categories to student profile field names."""
        FIELD_MAP = {
            "income": "annual_family_income",
            "marks": "marks_percentage",
            "cgpa": "cgpa",
            "age": "age_years",
            "category": "caste_category",
            "disability": "is_pwd",
            "domicile": "domicile_state",
            "state": "state",
            "course": "course_name",
            "education_level": "education_level",
        }
        # Try exact rule_key match first, then category
        if rule_key in FIELD_MAP:
            return FIELD_MAP[rule_key]
        return FIELD_MAP.get(rule_category)


# Singleton instance
eligibility_engine = EligibilityEngine()
