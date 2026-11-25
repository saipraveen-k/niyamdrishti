# Known Limitations

This document describes current limitations and areas for improvement. It is maintained honestly to set correct expectations for contributors and users.

---

## Eligibility evaluation

**Profile field coverage is partial.** The `EligibilityEngine._get_profile_field()` mapping covers the most common rule categories (income, marks, cgpa, age, category, disability, domicile, course, education level). Schemes with unusual eligibility criteria — such as employment status, land ownership, or specific bank account types — will return `UNKNOWN` for those rules.

**Compound rules have limited nesting.** The engine supports one level of `and`/`or` compound conditions. Deeply nested compound rules (e.g., `(A AND (B OR C)) AND D`) are only partially evaluated; inner nesting beyond the first level is not recursed.

**No "contains" / "any" operator.** The operator map lists `contains` and `any` in the docstring but they are not implemented. Rules with these operators return `UNKNOWN`.

**Match score is directional, not absolute.** The `match_score` percentage reflects passed vs failed *mandatory* rules only. Unknown (missing profile data) rules are excluded from the denominator, so a score of 100% can mask several unknowns.

---

## AI extraction

**Extraction accuracy depends on document quality.** Scanned PDFs with poor scan quality or non-standard fonts produce lower OCR confidence, which propagates to lower rule confidence scores. Always have a human reviewer approve rules before activating a version.

**Tables and eligibility matrices are tricky.** When scheme documents encode eligibility as a table (e.g., different income limits for different categories in the same cell), the LLM may extract a single rule instead of separate per-category rules.

**Telegu/Hindi documents.** OCR uses Tesseract with the English language pack by default. Install `tesseract-ocr-tel` and `tesseract-ocr-hin` packages and update the `TESSERACT_CMD` env var for better results with regional language documents.

---

## Policy comparison

**Rule matching is by (category, key) only.** If a document version renames a rule key (e.g., `annual_income` → `family_income`), the engine will report one REMOVED and one ADDED change instead of a MODIFIED change. The human summary will not reflect this.

**Comparison is not aware of units.** A change from `300000 INR` to `3 lakh` would be detected as a MODIFIED change because the values differ, even if they are economically equivalent.

---

## AI Assistant (RAG)

**Context window limits large schemes.** The assistant retrieves top-K chunks by vector similarity. Very large schemes with many versions may retrieve stale chunks if vector embeddings are not updated after a new version is approved.

**Citations reference page numbers from the extracted text, not the displayed PDF.** If the PDF viewer uses a different page numbering (e.g., with a cover page offset), cited page numbers may be off by one or more.

**No streaming in the current implementation.** The `/assistant/chat` endpoint returns a complete response. Streaming SSE can be added by switching to `StreamingResponse` in the router.

---

## Infrastructure

**Background document processing is not fully implemented.** The worker stubs exist in `app/workers/` but the job queue integration (Redis/Celery or similar) is not wired up in Phase 1. Document extraction must be triggered manually via the admin API in the current release.

**No rate limiting.** The API does not apply per-user rate limits. Add a Redis-backed rate limiter middleware before exposing to public traffic.

**Email notifications are stubbed.** The notifications module returns 501 responses. Connect to an SMTP provider or Supabase's email feature to activate.

---

## Scope

**AP/Telangana focus in seed data.** The seed script contains 4 representative schemes. Central schemes and other state schemes are not seeded. Admin users need to upload and extract rules for additional schemes.

**No offline mode.** The application requires a live API and Supabase connection. Progressive Web App / offline support is not implemented.
