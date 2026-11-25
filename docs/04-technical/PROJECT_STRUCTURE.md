# Project Structure

## Short Explanation

NiyamDrishti uses a two-app repository layout (`frontend/` and `backend/`) accompanied by shared deployment configs, setup scripts, and documentation.

---

## 1. Repository Tree (Observed Source Layout)

```text
NiyamDrishti/
├── .github/
│   └── workflows/
│       └── ci.yml                       # GitHub Actions CI (pytest, tsc, next build, pip-audit)
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI entry point, CORS, router mounting, /health
│   │   ├── core/
│   │   │   ├── config.py                # Pydantic Settings
│   │   │   ├── logging.py               # structlog setup
│   │   │   ├── permissions.py           # AppRole enum and role groups
│   │   │   └── security.py              # Supabase JWT validation, RoleChecker, require_roles
│   │   ├── database/
│   │   │   ├── database.py              # Async SQLAlchemy engine & get_db()
│   │   │   ├── types.py                 # Cross-dialect JSONB TypeDecorator (PG + SQLite)
│   │   │   ├── models/
│   │   │   │   ├── __init__.py          # Model registry (22 tables)
│   │   │   │   ├── base.py              # Base, UUIDMixin, TimestampMixin, SoftDeleteMixin
│   │   │   │   ├── user.py              # UserProfile, StudentProfile, College, CollegeMembership, AdminInvitation
│   │   │   │   ├── scheme.py            # Scheme, SchemeSource, SchemeVersion, SchemeDocument, SchemeRule, PolicyComparison, PolicyChangeEvent
│   │   │   │   ├── document.py          # DocumentUpload, DocumentProcessingJob, DocumentProcessingAttempt
│   │   │   │   └── application.py       # StudentSchemeEvaluation, SavedScheme, StudentImpact, ActionPlan, ActionTask, StudentApplication, ApplicationStatusHistory
│   │   │   └── migrations/
│   │   │       ├── env.py               # Async Alembic configuration
│   │   │       ├── script.py.mako
│   │   │       └── versions/            # Currently contains .gitkeep only
│   │   ├── ai/
│   │   │   ├── providers/
│   │   │   │   ├── base.py              # AIProvider ABC
│   │   │   │   └── openai_provider.py   # OpenAI structured outputs, chat, translate
│   │   │   └── schemas/
│   │   │       └── extraction.py        # ExtractedSchemeRules, ExtractedRule, ConditionValue
│   │   ├── modules/                     # 14 domain routers + services/engines
│   │   │   ├── applications/
│   │   │   ├── assistant/
│   │   │   ├── auth/
│   │   │   ├── changelens/              # comparison_engine.py + router.py
│   │   │   ├── documents/               # service.py + router.py
│   │   │   ├── eligibility/             # engine.py + router.py
│   │   │   ├── impact/
│   │   │   ├── lifemap/
│   │   │   ├── monitoring/
│   │   │   ├── notifications/
│   │   │   ├── profiles/
│   │   │   ├── reviews/
│   │   │   ├── schemes/                 # router.py, schemas.py, service.py
│   │   │   └── users/
│   │   └── workers/
│   │       └── __init__.py              # Empty placeholder for background workers
│   ├── scripts/
│   │   └── seed_schemes.py              # Seeds 4 sample AP/Telangana/All-India schemes
│   ├── tests/
│   │   ├── conftest.py                  # SQLite in-memory async test client fixture
│   │   ├── conftest_test.py             # Alternate conftest copy
│   │   ├── test_comparison_engine.py    # 14 ChangeLens unit tests
│   │   ├── test_eligibility_engine.py   # 15 EligibilityEngine unit tests
│   │   ├── test_health.py               # 5 HTTP smoke tests
│   │   └── test_sanity.py               # 1 sanity test
│   ├── .env.example
│   ├── alembic.ini
│   ├── Dockerfile                       # Multi-stage Python 3.11 + Tesseract + Poppler
│   ├── pytest.ini
│   ├── render.yaml                      # Render web service + Postgres spec
│   ├── requirements.txt
│   └── _fix_router.py                   # Leftover one-off formatting helper script
├── frontend/
│   ├── public/                          # SVG icons (file, globe, next, vercel, window)
│   ├── src/
│   │   ├── middleware.ts                # Supabase SSR route & role protection
│   │   ├── app/                         # Next.js App Router pages
│   │   │   ├── (auth)/login/page.tsx
│   │   │   ├── (auth)/register/page.tsx
│   │   │   ├── auth/callback/route.ts
│   │   │   ├── admin/page.tsx
│   │   │   ├── applications/page.tsx
│   │   │   ├── assistant/page.tsx
│   │   │   ├── changelens/page.tsx
│   │   │   ├── dashboard/
│   │   │   ├── eligibility/page.tsx
│   │   │   ├── lifemap/page.tsx
│   │   │   ├── reviewer/page.tsx
│   │   │   ├── schemes/
│   │   │   ├── settings/profile/page.tsx
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── features/                # change-event-card, criterion-result, scheme-card
│   │   │   ├── layout/                  # navbar.tsx, sidebar.tsx
│   │   │   ├── ui/                      # badge, button, card, input, skeleton
│   │   │   └── providers.tsx
│   │   ├── hooks/                       # use-auth.ts, use-schemes.ts
│   │   ├── lib/                         # api-client.ts, utils.ts, supabase/{client,server}.ts
│   │   └── types/index.ts
│   ├── .env.example
│   ├── eslint.config.mjs
│   ├── next.config.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── vercel.json
├── docs/                                # Comprehensive project documentation & diagrams
├── scripts/
│   └── setup.sh                         # Bash local environment bootstrap script
├── docker-compose.yml                   # Local dev stack (api, frontend, postgres, redis)
└── README.md
```

---

## Related Documentation

- [Technology Stack](TECHNOLOGY_STACK.md)
- [Backend Architecture](../03-architecture/BACKEND_ARCHITECTURE.md)
- [Frontend Architecture](../03-architecture/FRONTEND_ARCHITECTURE.md)

