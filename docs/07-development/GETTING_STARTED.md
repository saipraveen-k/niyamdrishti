# Getting Started

## Short Explanation

This guide helps a new developer run NiyamDrishti locally in minutes, whether using **Docker Compose** or running the **FastAPI** backend and **Next.js** frontend directly on your workstation.

---

## 1. Prerequisites

| Tool | Required Version | Verification Command |
|---|---|---|
| **Python** | `3.10+` (`3.11` recommended) | `python --version` |
| **Node.js & npm** | `20+` | `node --version && npm --version` |
| **Supabase Project** | Free tier supported | [supabase.com](https://supabase.com) (or local Postgres `16`) |
| **Docker** *(optional)* | Docker Desktop / Compose v2 | `docker compose version` |
| **Tesseract OCR** *(optional)* | System binary for scanned PDFs | `tesseract --version` |

---

## 2. Quickest Path (macOS / Linux / Git Bash)

```bash
git clone https://github.com/saipraveen-k/niyamdrishti.git
cd niyamdrishti
bash scripts/setup.sh
```

`scripts/setup.sh` copies `.env.example` files if missing, creates `backend/venv`, installs `backend/requirements.txt`, and runs `npm install` in `frontend/`.

On Windows PowerShell, follow the explicit steps in [Local Setup](LOCAL_SETUP.md), [Backend Setup](BACKEND_SETUP.md), and [Frontend Setup](FRONTEND_SETUP.md).

---

## 3. Verification Checklist

Once running:
1. Open backend health check: `http://localhost:8000/health` → `{"status": "ok", ...}`
2. Open Swagger docs (dev only): `http://localhost:8000/api/docs`
3. Open frontend app: `http://localhost:3000`

---

## Related Documentation

- [Local Setup](LOCAL_SETUP.md)
- [Environment Variables](ENVIRONMENT_VARIABLES.md)
- [Docker Setup](DOCKER_SETUP.md)
- [Database Setup](DATABASE_SETUP.md)

