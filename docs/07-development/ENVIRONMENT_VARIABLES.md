# Environment Variables

## Short Explanation

All backend environment variables are validated at startup by `Settings(BaseSettings)` in `backend/app/core/config.py`, and frontend public variables are loaded from `frontend/.env.local`. Never commit `.env` or `.env.local` files to Git.

---

## 1. Backend Variables (`backend/.env.example`)

| Variable | Required | Default / Example | Usage in Code (`config.py`) |
|---|---|---|---|
| `APP_NAME` | No | `NiyamDrishti` | Returned by `GET /health` |
| `APP_ENV` | No | `development` (`development\|staging\|production`) | Controls OpenAPI docs visibility & logging colors |
| `DEBUG` | No | `false` (`true` in `.env.example`) | Enables SQLAlchemy SQL echo |
| `SECRET_KEY` | **Yes** | Min `32` chars | Required by `Settings` (`Field(min_length=32)`) |
| `FRONTEND_URL` | No | `http://localhost:3000` | Frontend base URL |
| `ALLOWED_ORIGINS` | No | `http://localhost:3000` | Comma-separated CORS origins (`cors_origins_list`) |
| `SUPABASE_URL` | **Yes** | `https://your-project.supabase.co` | Used by `verify_supabase_token` |
| `SUPABASE_ANON_KEY` | **Yes** | `your-supabase-anon-key` | Sent as `apikey` header to Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | **Yes** | `your-supabase-service-role-key` | Server-only key (never expose to browser) |
| `DATABASE_URL` | **Yes** | `postgresql+asyncpg://...` | Async SQLAlchemy connection string |
| `DATABASE_URL_SYNC` | No | `postgresql://...` | Sync URL used by Alembic `env.py` |
| `AI_PROVIDER` | No | `openai` (`openai\|anthropic`) | Selects provider in `ai_available` |
| `OPENAI_API_KEY` | Optional | `sk-...` | Enables `OpenAIProvider` |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Chat & translation model |
| `OPENAI_EXTRACTION_MODEL` | No | `gpt-4o` | Structured rule extraction model |
| `ANTHROPIC_API_KEY` | Optional | `sk-ant-...` | Configured in `Settings`; provider class not implemented yet |
| `ANTHROPIC_MODEL` / `ANTHROPIC_EXTRACTION_MODEL` | No | `claude-3-5-haiku-20241022` / `claude-3-5-sonnet-20241022` | Configured in `Settings` |
| `MAX_UPLOAD_SIZE_BYTES` | No | `20971520` (20 MB) | Enforced by `validate_upload()` |
| `MAX_PDF_PAGES` | No | `200` | Enforced by `extract_text_from_pdf()` |
| `TESSERACT_CMD` | Optional | Empty | Custom path to `tesseract` executable |
| `OCR_MIN_CONFIDENCE` | No | `60` | Configured in `Settings` |
| `OFFICIAL_DOCS_BUCKET`, `STUDENT_UPLOADS_BUCKET`, `REPORTS_BUCKET` | No | `official-documents`, `student-uploads`, `generated-reports` | Bucket names |
| `SIGNED_URL_EXPIRY` | No | `3600` | Seconds |
| `STUDENT_DOC_RETENTION_DAYS` | No | `30` | Retention policy days |
| `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `LOGIN_MAX_ATTEMPTS`, `LOGIN_ATTEMPT_WINDOW_MINUTES` | No | `60`, `30`, `5`, `15` | Configured in `Settings` (auth managed by Supabase) |
| `EMAIL_PROVIDER`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `FROM_EMAIL`, `FROM_NAME` | Optional | `supabase_smtp`, `587`, `noreply@niyamdrishti.in` | Email configuration (notifications currently stubbed) |
| `LOG_LEVEL`, `LOG_FORMAT` | No | `INFO`, `console` (`json\|console`) | `structlog` configuration |
| `WORKER_POLL_INTERVAL`, `WORKER_MAX_RETRIES`, `WORKER_RETRY_BACKOFF_SECONDS` | No | `5`, `3`, `60` | Worker config (worker not yet implemented) |

> [!NOTE]
> `backend/.env.example` also lists `CORS_ORIGINS` and commented `TWILIO_*` variables, whereas `config.py` reads `ALLOWED_ORIGINS` (ignoring `extra` env keys).

---

## 2. Frontend Variables (`frontend/.env.example`)

| Variable | Required | Default / Example | Usage |
|---|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | **Yes** | `https://your-project.supabase.co` | Supabase SSR & browser client |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | **Yes** | `your-supabase-anon-key` | Supabase SSR & browser client |
| `NEXT_PUBLIC_API_URL` | **Yes** | `http://localhost:8000` | Base URL for `apiClient` (`/api/v1` appended) |
| `NEXT_PUBLIC_APP_NAME` | No | `NiyamDrishti` | App display metadata |
| `NEXT_PUBLIC_APP_ENV` | No | `development` | Environment label |

---

## Related Documentation

- [Local Setup](LOCAL_SETUP.md)
- [Security](../04-technical/SECURITY.md)
- [Deployment Overview](../09-deployment-and-devops/DEPLOYMENT_OVERVIEW.md)

