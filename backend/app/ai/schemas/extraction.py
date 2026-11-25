"""
Pydantic schemas for LLM-extracted scheme rule data.
All extraction outputs are validated against these before being stored.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RuleOperator(str, Enum):
    LTE = "lte"      # less than or equal
    LT = "lt"        # less than
    GTE = "gte"      # greater than or equal
    GT = "gt"        # greater than
    EQ = "eq"        # equal
    NEQ = "neq"      # not equal
    IN = "in"        # value is in list
    NOT_IN = "not_in"
    ANY = "any"      # no specific operator (existence check)


class RuleCategory(str, Enum):
    INCOME = "income"
    MARKS = "marks"
    CGPA = "cgpa"
    AGE = "age"
    CATEGORY = "category"
    DISABILITY = "disability"
    DOMICILE = "domicile"
    STATE = "state"
    COURSE = "course"
    EDUCATION_LEVEL = "education_level"
    AMOUNT = "amount"
    DEADLINE = "deadline"
    DOCUMENT = "document"
    RENEWAL = "renewal"
    EXCLUSION = "exclusion"
    OTHER = "other"


class ConditionValue(BaseModel):
    operator: RuleOperator
    value: float | int | str | List[str] | None = None
    unit: Optional[str] = None  # inr|percent|cgpa|years
    logic: Optional[str] = None  # and|or (for compound conditions)
    sub_conditions: Optional[List["ConditionValue"]] = None
    note: Optional[str] = None  # human-readable explanation


ConditionValue.model_rebuild()


class ExtractedRule(BaseModel):
    rule_category: RuleCategory
    rule_key: str = Field(
        description="Short identifier, e.g. 'annual_family_income', 'minimum_marks'"
    )
    condition: ConditionValue
    is_mandatory: bool = True
    source_text: Optional[str] = Field(
        None,
        description="Verbatim text from document supporting this rule",
    )
    source_page: Optional[int] = Field(None, description="1-indexed page number")
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Extraction confidence 0-1",
    )
    notes: Optional[str] = None


class ExtractedSchemeRules(BaseModel):
    """
    Top-level extraction result for a scheme notification document.
    Validated by Pydantic before storage.
    """

    scheme_name: str
    department: Optional[str] = None
    scheme_identifier: Optional[str] = None
    state: Optional[str] = None

    # Key metadata
    scholarship_amount: Optional[str] = None
    application_start_date: Optional[str] = None
    application_end_date: Optional[str] = None
    official_url: Optional[str] = None
    application_url: Optional[str] = None

    # Eligibility rules
    rules: List[ExtractedRule]

    # Required documents
    required_documents: List[str] = Field(default_factory=list)

    # Application procedure
    application_procedure: Optional[str] = None

    # Renewal conditions
    renewal_conditions: Optional[str] = None

    # Extraction metadata
    extraction_notes: Optional[str] = Field(
        None,
        description="Any ambiguities or extraction caveats",
    )
    overall_confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )
