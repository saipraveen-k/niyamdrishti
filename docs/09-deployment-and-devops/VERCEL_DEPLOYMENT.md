# Vercel Deployment

## Short Explanation

The Next.js 16 frontend is pre-configured for Vercel deployment via `frontend/vercel.json`, including region pinning (`sin1`), security headers, and `/api/:path*` backend rewrites.

---

## 1. Configuration (`frontend/vercel.json`)

| Key | Configured Value | Notes |
|---|---|---|
| `framework` | `nextjs` | Auto-detected Next.js build |
| `buildCommand` | `npm run build` | Production build |
| `outputDirectory` | `.next` | Next.js build output |
| `regions` | `["sin1"]` | Singapore edge/serverless region |
| `env` | `@niyamdrishti_api_url`, `@niyamdrishti_supabase_url`, `@niyamdrishti_supabase_anon_key` | Mapped in Vercel Project Settings |
| `headers` | `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()` | Applied to `/(.*)` |
| `rewrites` | `/api/:path*` → `https://niyamdrishti-api.onrender.com/api/:path*` | Update destination to match your Render service URL |

---

## 2. Deployment Steps

1. Import the GitHub repository in Vercel and set **Root Directory** to `frontend`.
2. Configure environment variables (`NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`).
3. Verify `vercel.json` `rewrites[0].destination` points to your live Render backend URL.
4. Deploy. *(Note: `npm run build` in Next.js 16 runs TypeScript checking; verify ESLint errors do not block builds or resolve the 9 ESLint errors documented in [Test Results](../08-testing-and-quality/TEST_RESULTS.md).)*

---

## Related Documentation

- [Deployment Overview](DEPLOYMENT_OVERVIEW.md)
- [Render Deployment](RENDER_DEPLOYMENT.md)
- [Frontend Setup](../07-development/FRONTEND_SETUP.md)

