# Docker Setup

## Short Explanation

`docker-compose.yml` defines a 4-service local development stack (`api`, `frontend`, `postgres`, and optional `redis`) so contributors can spin up the full environment with one command.

---

## 1. Compose Services (`docker-compose.yml`)

| Service | Image / Build | Port | Purpose |
|---|---|---|---|
| `api` | Built from `./backend/Dockerfile` (`target: runtime`) | `8000:8000` | FastAPI with live `--reload` mount (`./backend:/app`) |
| `frontend` | `node:20-alpine` | `3000:3000` | Runs `npm install && npm run dev` |
| `postgres` | `postgres:16-alpine` | `5432:5432` | Local PostgreSQL 16 (`niyamdrishti` / `devpassword`) |
| `redis` | `redis:7-alpine` | `6379:6379` | Optional Redis container (currently unused by backend code) |

---

## 2. Usage

1. Ensure `backend/.env` and `frontend/.env` exist (`docker-compose.yml` references `./frontend/.env` in `env_file`, unlike local Next.js which uses `.env.local`).
2. Start services:
   ```bash
   docker compose up --build
   ```
3. Stop services:
   ```bash
   docker compose down
   ```

---

## Related Documentation

- [Docker Architecture](../09-deployment-and-devops/DOCKER_ARCHITECTURE.md)
- [Local Setup](LOCAL_SETUP.md)

