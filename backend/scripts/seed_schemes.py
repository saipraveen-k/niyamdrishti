"""
Seed script: populate the database with representative scheme data for development.

Usage:
    cd backend
    python -m scripts.seed_schemes

Requires DATABASE_URL and other env vars to be set (copy .env.example → .env).
"""

import asyncio
import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.database.models.scheme import Scheme, SchemeVersion, SchemeRule


SCHEMES = [
    {
        "name": "Post Matric Scholarship for SC Students — Andhra Pradesh",
        "slug": "ap-post-matric-sc-scholarship",
        "description": (
            "Financial assistance for SC students pursuing post-matriculation "
            "courses in Andhra Pradesh. Covers tuition, maintenance, and study "
            "material allowances."
        ),
        "department": "AP Social Welfare Department",
        "scheme_identifier": "AP-SW-PMS-SC-2024",
        "state": "Andhra Pradesh",
        "scheme_type": "scholarship",
        "is_active": True,
        "is_published": True,
        "official_url": "https://apswreis.apcfss.in/",
        "latest_amount": 15000.00,
        "rules": [
            {
                "rule_category": "category",
                "rule_key": "category",
                "condition": {"operator": "in", "value": ["SC"], "unit": None},
                "source_text": "The scheme is exclusively for Scheduled Caste students.",
                "source_page": 1,
                "confidence": 0.98,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "income",
                "rule_key": "income",
                "condition": {"operator": "lte", "value": 250000, "unit": "inr"},
                "source_text": "Annual family income shall not exceed Rs. 2.50 lakh.",
                "source_page": 2,
                "confidence": 0.97,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "domicile",
                "rule_key": "domicile_state",
                "condition": {"operator": "eq", "value": "Andhra Pradesh"},
                "source_text": "Applicant must be a domicile of Andhra Pradesh.",
                "source_page": 2,
                "confidence": 0.95,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "marks",
                "rule_key": "marks",
                "condition": {"operator": "gte", "value": 50, "unit": "percent"},
                "source_text": "Minimum 50% marks in previous qualifying examination.",
                "source_page": 3,
                "confidence": 0.93,
                "is_mandatory": True,
                "review_status": "approved",
            },
        ],
    },
    {
        "name": "Dr. YSR Vidyadeeepika Scholarship — Telangana",
        "slug": "ts-ysr-vidyadeepika",
        "description": (
            "Merit-cum-means scholarship for students from BC, SC, ST and EBC "
            "communities pursuing professional courses in Telangana."
        ),
        "department": "Telangana BC Welfare Department",
        "scheme_identifier": "TS-BCW-VD-2024",
        "state": "Telangana",
        "scheme_type": "scholarship",
        "is_active": True,
        "is_published": True,
        "official_url": "https://telanganaepass.cgg.gov.in/",
        "latest_amount": 20000.00,
        "rules": [
            {
                "rule_category": "category",
                "rule_key": "category",
                "condition": {
                    "operator": "in",
                    "value": ["BC-A", "BC-B", "BC-C", "BC-D", "BC-E", "SC", "ST", "EBC"],
                },
                "source_text": "Open to BC, SC, ST and EBC students.",
                "source_page": 1,
                "confidence": 0.97,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "income",
                "rule_key": "income",
                "condition": {"operator": "lte", "value": 200000, "unit": "inr"},
                "source_text": "Family income limit: Rs. 2 lakh per annum.",
                "source_page": 2,
                "confidence": 0.96,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "domicile",
                "rule_key": "domicile_state",
                "condition": {"operator": "eq", "value": "Telangana"},
                "source_text": "Local candidate of Telangana state.",
                "source_page": 2,
                "confidence": 0.95,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "marks",
                "rule_key": "marks",
                "condition": {"operator": "gte", "value": 60, "unit": "percent"},
                "source_text": "60% or above in the qualifying examination.",
                "source_page": 3,
                "confidence": 0.94,
                "is_mandatory": True,
                "review_status": "approved",
            },
        ],
    },
    {
        "name": "National Merit Scholarship — Central Government",
        "slug": "central-national-merit-scholarship",
        "description": (
            "Merit-based scholarship for Class 11 and 12 students who scored "
            "above 80% marks in Class 10 board examination. Available nationwide."
        ),
        "department": "Ministry of Education, Government of India",
        "scheme_identifier": "MOE-NMS-2024",
        "state": "All India",
        "scheme_type": "scholarship",
        "is_active": True,
        "is_published": True,
        "official_url": "https://scholarships.gov.in/",
        "latest_amount": 12000.00,
        "rules": [
            {
                "rule_category": "marks",
                "rule_key": "marks",
                "condition": {"operator": "gte", "value": 80, "unit": "percent"},
                "source_text": (
                    "Students who have secured 80% or above marks in Class X "
                    "board examination."
                ),
                "source_page": 1,
                "confidence": 0.99,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "income",
                "rule_key": "income",
                "condition": {"operator": "lte", "value": 150000, "unit": "inr"},
                "source_text": "Family income should not exceed Rs. 1.5 lakh per annum.",
                "source_page": 2,
                "confidence": 0.98,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "education_level",
                "rule_key": "education_level",
                "condition": {
                    "operator": "in",
                    "value": ["class_11", "class_12"],
                },
                "source_text": "Students studying in Class XI or XII.",
                "source_page": 1,
                "confidence": 0.97,
                "is_mandatory": True,
                "review_status": "approved",
            },
        ],
    },
    {
        "name": "Prime Minister's Research Fellowship",
        "slug": "pmrf-phd-fellowship",
        "description": (
            "Fellowship for direct PhD admission at IITs/IISc for outstanding "
            "BTech/BE/BS/MSc graduates. Provides monthly stipend and research grant."
        ),
        "department": "Ministry of Education, Government of India",
        "scheme_identifier": "MOE-PMRF-2024",
        "state": "All India",
        "scheme_type": "fellowship",
        "is_active": True,
        "is_published": True,
        "official_url": "https://www.pmrf.in/",
        "latest_amount": 70000.00,
        "rules": [
            {
                "rule_category": "cgpa",
                "rule_key": "cgpa",
                "condition": {"operator": "gte", "value": 8.0, "unit": "cgpa"},
                "source_text": "Minimum CGPA of 8.0 on a 10-point scale.",
                "source_page": 2,
                "confidence": 0.99,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "education_level",
                "rule_key": "education_level",
                "condition": {
                    "operator": "in",
                    "value": ["btech", "be", "bs", "msc", "integrated_msc"],
                },
                "source_text": "Candidates with BTech/BE/BS/MSc or Integrated MSc.",
                "source_page": 2,
                "confidence": 0.97,
                "is_mandatory": True,
                "review_status": "approved",
            },
            {
                "rule_category": "age",
                "rule_key": "age",
                "condition": {"operator": "lte", "value": 30, "unit": "years"},
                "source_text": "Age limit: 30 years as on the date of application.",
                "source_page": 3,
                "confidence": 0.95,
                "is_mandatory": True,
                "review_status": "approved",
            },
        ],
    },
]


async def seed(session: AsyncSession) -> None:
    print("Seeding schemes...")
    for scheme_data in SCHEMES:
        rules_data = scheme_data.pop("rules")

        scheme = Scheme(
            id=uuid.uuid4(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            **{k: v for k, v in scheme_data.items() if k != "latest_amount"},
            latest_amount=scheme_data.get("latest_amount"),
        )
        session.add(scheme)
        await session.flush()  # get scheme.id

        version = SchemeVersion(
            id=uuid.uuid4(),
            scheme_id=scheme.id,
            version_number=1,
            version_label="v1.0 — seed",
            is_active=True,
            is_approved=True,
            approved_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(version)
        await session.flush()

        for rd in rules_data:
            rule = SchemeRule(
                id=uuid.uuid4(),
                version_id=version.id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                **rd,
            )
            session.add(rule)

        scheme.latest_version_id = version.id

    await session.commit()
    print(f"Seeded {len(SCHEMES)} schemes with rules.")


async def main() -> None:
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        await seed(session)
    await engine.dispose()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
