"""
Application roles and permission constants.
"""

from enum import Enum


class AppRole(str, Enum):
    STUDENT = "student"
    COLLEGE_COORDINATOR = "college_coordinator"
    DOCUMENT_REVIEWER = "document_reviewer"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


# Groups for common permission checks
ADMIN_ROLES = {AppRole.ADMIN, AppRole.SUPER_ADMIN}
REVIEWER_ROLES = {AppRole.DOCUMENT_REVIEWER, AppRole.ADMIN, AppRole.SUPER_ADMIN}
COORDINATOR_ROLES = {AppRole.COLLEGE_COORDINATOR, AppRole.ADMIN, AppRole.SUPER_ADMIN}
ALL_STAFF_ROLES = {
    AppRole.COLLEGE_COORDINATOR,
    AppRole.DOCUMENT_REVIEWER,
    AppRole.ADMIN,
    AppRole.SUPER_ADMIN,
}
ALL_ROLES = set(AppRole)
