"""
Export all models for Alembic autodiscovery.
"""

from app.database.models.base import Base
from app.database.models.user import (
    AdminInvitation,
    College,
    CollegeMembership,
    StudentProfile,
    UserProfile,
)
from app.database.models.scheme import (
    PolicyChangeEvent,
    PolicyComparison,
    Scheme,
    SchemeDocument,
    SchemeRule,
    SchemeSource,
    SchemeVersion,
)
from app.database.models.document import (
    DocumentProcessingAttempt,
    DocumentProcessingJob,
    DocumentUpload,
)
from app.database.models.application import (
    ActionPlan,
    ActionTask,
    ApplicationStatusHistory,
    SavedScheme,
    StudentApplication,
    StudentImpact,
    StudentSchemeEvaluation,
)

__all__ = [
    "Base",
    "UserProfile",
    "StudentProfile",
    "College",
    "CollegeMembership",
    "AdminInvitation",
    "Scheme",
    "SchemeSource",
    "SchemeVersion",
    "SchemeDocument",
    "SchemeRule",
    "PolicyComparison",
    "PolicyChangeEvent",
    "DocumentUpload",
    "DocumentProcessingJob",
    "DocumentProcessingAttempt",
    "StudentSchemeEvaluation",
    "SavedScheme",
    "StudentImpact",
    "ActionPlan",
    "ActionTask",
    "StudentApplication",
    "ApplicationStatusHistory",
]
