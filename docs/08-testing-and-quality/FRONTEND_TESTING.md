# Frontend Testing

## Short Explanation

The frontend currently relies on **TypeScript type checking** (`tsc --noEmit`) and **ESLint** (`npm run lint`); while Jest, React Testing Library, and Playwright are listed in `frontend/package.json`, no component or E2E test suites have been authored yet.

---

## 1. Static Checks Observed on 2026-11-25

| Check | Command | Result | Details |
|---|---|---|---|
| **TypeScript** | `npx tsc --noEmit` | **Passed** (`exit 0`) | Zero TypeScript errors |
| **ESLint** | `npm run lint` | **Failed** (`exit 1`) | **27 problems (9 errors, 18 warnings)** — primarily `react-hooks/set-state-in-effect` in `assistant/page.tsx`, `reviewer/page.tsx`, `use-schemes.ts`; `@typescript-eslint/no-explicit-any`; `@typescript-eslint/no-empty-object-type` in `card.tsx`; unused imports; and `@next/next/no-location-assign-relative-destination` warnings |
| **Next.js Build** | `npm run build` | Configured in CI | Runs in `.github/workflows/ci.yml` with dummy `NEXT_PUBLIC_*` test env vars |

---

## 2. Installed but Unused Test Frameworks (`frontend/package.json`)

- `jest` (`^30.5.2`) & `jest-environment-jsdom` (`^30.5.2`)
- `@testing-library/react` (`^16.3.3`) & `@testing-library/jest-dom` (`^8.0.0`)
- `@playwright/test` (`^1.65.1`)

No `jest.config.*`, `playwright.config.*`, `*.test.tsx`, or `*.spec.ts` files exist in `frontend/` yet.

---

## Related Documentation

- [Test Results](TEST_RESULTS.md)
- [Frontend Architecture](../03-architecture/FRONTEND_ARCHITECTURE.md)
- [CI/CD Pipeline](../09-deployment-and-devops/CI_CD_PIPELINE.md)

