# Visual Assets & Screenshot Checklist

> [!NOTE]
> No application screenshots are currently committed in `docs/assets/screenshots/`. Per project documentation standards, synthetic or fabricated screenshots are **not** included. Use this checklist to capture real screenshots from a running local instance.

---

## 1. Directory Organization

- `docs/assets/screenshots/` — Live UI captures from the running Next.js frontend
- `docs/assets/images/` — Supporting graphics and logos
- `docs/assets/architecture/` — Exported PNG/SVG architecture renders (if exported from `docs/diagrams/*.mmd`)

---

## 2. Recommended Screenshot Checklist

| # | Screen / View | Frontend Route | Status | Target Filename |
|---|---|---|---|---|
| 1 | Landing page | `/` | Missing | `01-landing-page.png` |
| 2 | Student dashboard | `/dashboard` | Missing | `02-student-dashboard.png` |
| 3 | Scheme discovery | `/schemes` | Missing | `03-scheme-discovery.png` |
| 4 | Eligibility results | `/eligibility` | Missing | `04-eligibility-results.png` |
| 5 | ChangeLens comparison | `/changelens` | Missing | `05-changelens-comparison.png` |
| 6 | LifeMap action plan | `/lifemap` | Missing | `06-lifemap.png` |
| 7 | AI Assistant chat | `/assistant` | Missing | `07-ai-assistant.png` |
| 8 | Admin dashboard | `/admin` | Missing | `08-admin-dashboard.png` |
| 9 | Document reviewer queue | `/reviewer` | Missing | `09-reviewer-queue.png` |
| 10 | Mobile responsive view | `/` & `/dashboard` (`390x844`) | Missing | `10-mobile-responsive.png` |

---

## 3. How to Capture Screenshots Locally

1. Start the backend and seed schemes:
   ```bash
   cd backend
   python -m scripts.seed_schemes
   uvicorn app.main:app --reload
   ```
2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```
3. Open `http://localhost:3000` in your browser using a **synthetic test account** (never capture real student PII or API keys).
4. Capture full-page and mobile (`390x844` DevTools viewport) screenshots and save them under `docs/assets/screenshots/` using the filenames above.
5. Reference them in Markdown with relative paths (e.g., `![Landing Page](docs/assets/screenshots/01-landing-page.png)`).

> [!TIP]
> Until screenshots are captured, all architectural and product workflows are visualized using GitHub-native Mermaid diagrams under `docs/diagrams/`.

