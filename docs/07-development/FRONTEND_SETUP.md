# Frontend Setup

## Short Explanation

The Next.js 16 frontend runs on Node.js 20+ and uses npm scripts defined in `frontend/package.json`.

---

## 1. Install Dependencies & Configure Env

```bash
cd frontend
cp .env.example .env.local
npm install
```

Populate `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, and `NEXT_PUBLIC_API_URL` in `frontend/.env.local`.

---

## 2. Available npm Scripts (`frontend/package.json`)

| Command | Action |
|---|---|
| `npm run dev` | Starts Next.js development server (`http://localhost:3000`) |
| `npm run build` | Builds production bundle (`.next/`) |
| `npm run start` | Serves production build |
| `npm run lint` | Runs `eslint` (currently exits with 9 errors, 18 warnings) |
| `npx tsc --noEmit` | Runs TypeScript compiler check (currently passes with 0 errors) |

---

## Related Documentation

- [Frontend Architecture](../03-architecture/FRONTEND_ARCHITECTURE.md)
- [Frontend Testing](../08-testing-and-quality/FRONTEND_TESTING.md)
- [Vercel Deployment](../09-deployment-and-devops/VERCEL_DEPLOYMENT.md)

