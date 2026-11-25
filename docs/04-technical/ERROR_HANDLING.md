# Error Handling

## Short Explanation

NiyamDrishti relies on FastAPI's built-in `HTTPException` and Pydantic validation error handlers on the backend, combined with Axios interceptors and `react-hot-toast` notifications on the frontend.

---

## 1. Backend Error Handling Patterns

| Status Code | Where Raised | Example Triggers |
|---|---|---|
| `401 Unauthorized` | `app/core/security.py` | Missing Bearer token or non-200 from Supabase `/auth/v1/user` |
| `403 Forbidden` | `RoleChecker` (`security.py`) | Authenticated user lacks required `app_role` |
| `404 Not Found` | `schemes`, `users`, `profiles`, `documents`, `changelens`, `reviews`, `applications` | Resource UUID missing or unpublished scheme accessed by non-admin |
| `409 Conflict` | `profiles/router.py` | `POST /profiles` when a `StudentProfile` already exists for the user |
| `422 Unprocessable Entity` | FastAPI/Pydantic + `documents`, `eligibility`, `changelens` | Invalid payload schema, invalid upload file/magic bytes, no approved rules/versions, or missing student profile on evaluation |
| `503 Service Unavailable` | `assistant/router.py` | Unhandled exception calling `OpenAIProvider.chat()` |

### Database Transaction Safety (`app/database/database.py`)

`get_db()` wraps every request session in `try / commit / except: rollback / finally: close`, preventing partial writes from persisting if an endpoint raises an exception.

### Graceful Degradation

- **AI Unavailable**: `POST /api/v1/assistant/chat` checks `settings.ai_available` and returns a friendly `200 OK` message instead of crashing when API keys are absent.
- **OCR / Document Parsing**: `documents/service.py` catches `ImportError` and `TesseractError` (falling back from `eng+tel` to `eng`), logging structured errors via `structlog`.

---

## 2. Frontend Error Handling Patterns

- **Axios 401 Interceptor (`src/lib/api-client.ts`)**: Clears `nd_access_token` from `localStorage` and redirects to `/login`.
- **Toast Feedback (`react-hot-toast`)**: Used across `login`, `register`, `settings/profile`, `reviewer`, `applications`, and `schemes/[id]`.
- **Empty & Error States**: `schemes/page.tsx` renders a retry button when the backend is unreachable; `eligibility/page.tsx` handles missing profiles (note: checks `404` whereas backend currently returns `422`).

---

## Related Documentation

- [API Response Format](../05-database-and-api/API_RESPONSE_FORMAT.md)
- [API Reference](../05-database-and-api/API_REFERENCE.md)
- [Backend Architecture](../03-architecture/BACKEND_ARCHITECTURE.md)

