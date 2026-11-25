# Technology Stack

## Short Explanation

This page lists the exact packages, versions, and tools verified directly from `frontend/package.json`, `backend/requirements.txt`, `backend/Dockerfile`, `docker-compose.yml`, and `.github/workflows/ci.yml`.

---

## 1. Frontend Stack (`frontend/package.json`)

| Category | Package | Version | Purpose |
|---|---|---|---|
| **Framework** | `next` | `16.4.6` | App Router, SSR middleware, Turbopack |
| **UI Library** | `react`, `react-dom` | `19.3.0` | Component rendering |
| **Language** | `typescript` | `^5` | Static type safety |
| **Styling** | `tailwindcss`, `@tailwindcss/turbopack` | `4.3.3` | Utility-first CSS & CSS theme tokens |
| **Auth / BaaS** | `@supabase/ssr`, `@supabase/supabase-js` | `^0.12.7`, `^2.119.2` | Browser/server Supabase auth & session cookies |
| **HTTP Client** | `axios` | `^1.21.1` | REST calls to FastAPI `/api/v1` |
| **Forms & Validation** | `react-hook-form`, `@hookform/resolvers`, `zod` | `^7.92.0`, `^7.0.9`, `^4.6.7` | Form handling & schema validation |
| **UI & Charts** | `lucide-react`, `framer-motion`, `recharts`, `next-themes`, `react-hot-toast` | `^1.80.0`, `^14.14.0`, `^3.11.1`, `^0.4.6`, `^2.6.1` | Icons, animations, charts, dark mode, toasts |
| **Utilities** | `clsx`, `tailwind-merge`, `date-fns` | `^2.1.1`, `^3.7.1`, `^4.4.0` | Class merging & date utilities |
| **Lint & Test (Dev)** | `eslint`, `eslint-config-next`, `jest`, `@testing-library/react`, `@playwright/test` | `^9`, `16.4.6`, `^30.5.2`, `^16.3.3`, `^1.65.1` | Linting active; Jest/Playwright test suites not yet written |

---

## 2. Backend Stack (`backend/requirements.txt`)

| Category | Package | Version | Purpose |
|---|---|---|---|
| **Web Framework** | `fastapi`, `uvicorn[standard]`, `starlette` | `0.115.0`, `0.32.0`, `0.41.0` | Async REST API server |
| **Validation** | `pydantic`, `pydantic-settings`, `email-validator` | `2.10.0`, `2.6.0`, `2.2.0` | Schemas & `.env` configuration |
| **Database & ORM** | `sqlalchemy`, `alembic`, `asyncpg`, `greenlet` | `2.0.36`, `1.14.0`, `0.30.0`, `3.1.1` | Async PostgreSQL ORM & migrations |
| **Supabase** | `supabase` | `2.10.0` | Supabase SDK (Storage/Auth integration) |
| **HTTP & Resilience** | `httpx`, `aiofiles`, `tenacity` | `0.28.0`, `24.1.0`, `9.0.0` | Remote token checks & async I/O |
| **Security & Auth** | `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`, `cryptography` | `3.3.0`, `1.7.4`, `0.0.12`, `43.0.3` | Multipart uploads & crypto primitives |
| **Logging** | `structlog` | `24.4.0` | JSON / console structured logging |
| **Document & OCR** | `PyMuPDF`, `pytesseract`, `Pillow`, `python-docx`, `beautifulsoup4`, `lxml` | `1.25.0`, `0.3.13`, `11.0.0`, `1.1.2`, `4.12.3`, `5.3.0` | PDF, DOCX, and image text extraction |
| **AI Providers** | `openai`, `anthropic`, `tiktoken` | `1.57.0`, `0.40.0`, `0.8.0` | `OpenAIProvider` active; `anthropic` not yet wired |
| **Concurrency** | `asyncio-throttle` | `1.0.2` | Declared for background job throttling |
| **Testing** | `pytest`, `pytest-asyncio`, `pytest-cov`, `anyio` | `8.3.3` (`9.2.0` in local venv), `0.24.0`, `6.0.0`, `4.7.0` | Unit & API test runner |

---

## 3. Infrastructure & DevOps

| Component | Version / Platform | Source |
|---|---|---|
| **Python Runtime** | `3.11` (Docker & CI) / `3.10+` (`3.10.11` local venv) | `backend/Dockerfile`, `.github/workflows/ci.yml` |
| **Node.js Runtime** | `20` (`node:20-alpine`) | `docker-compose.yml`, `.github/workflows/ci.yml` |
| **Database** | PostgreSQL `16` (`postgres:16-alpine` local / Supabase cloud) | `docker-compose.yml` |
| **System OCR Tools** | `tesseract-ocr`, `tesseract-ocr-eng`, `poppler-utils` | `backend/Dockerfile` |
| **Hosting** | Vercel (`sin1`) + Render (`singapore`) + Supabase (`ap-southeast-1`) | `frontend/vercel.json`, `backend/render.yaml`, `docs/DEPLOYMENT.md` |
| **CI** | GitHub Actions (`push`/`pull_request` on `main`, `develop`) | `.github/workflows/ci.yml` |

> [!NOTE]
> `docker-compose.yml` also defines `redis:7-alpine`, though no Python Redis client is installed or used in the current codebase.

---

## Related Documentation

- [Project Structure](PROJECT_STRUCTURE.md)
- [System Architecture](../03-architecture/SYSTEM_ARCHITECTURE.md)
- [Local Setup](../07-development/LOCAL_SETUP.md)

