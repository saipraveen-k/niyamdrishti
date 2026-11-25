# Multilingual Support

## Short Explanation

NiyamDrishti targets students in Andhra Pradesh, Telangana, and across India by supporting **English (`en`)**, **Telugu (`te`)**, and **Hindi (`hi`)** across user preferences, AI Assistant prompts, translation helpers, and OCR configuration.

---

## 1. Where Multilingual Support Exists in Code

| Layer | File | Details |
|---|---|---|
| **User Preference** | `models/user.py`, `frontend/src/types/index.ts` | `UserProfile.preferred_language` (`"en"` default), `Language = "en" \| "te" \| "hi"` |
| **AI Assistant Chat** | `backend/app/modules/assistant/router.py` | `ChatRequest.language` (`"en"`, `"te"`, `"hi"`); appends `"Please respond in Telugu (తెలుగు)."` or `"Please respond in Hindi (हिंदी)."` to the last message |
| **Translation Method** | `backend/app/ai/providers/openai_provider.py` | `OpenAIProvider.translate(text, target_language, context)` maps `te` → Telugu, `hi` → Hindi, `en` → English while preserving proper nouns |
| **Document OCR** | `backend/app/modules/documents/service.py` | `_ocr_pdf_pages()` and `extract_text_from_image()` attempt `pytesseract.image_to_string(img, lang="eng+tel")` before falling back to `lang="eng"` |

---

## 2. Current Limitations

- **Frontend UI Locale**: All Next.js UI navigation, labels, and forms are currently in English; `frontend/src/app/assistant/page.tsx` does not yet expose a language selector for `ChatRequest.language`.
- **Docker OCR Packs**: `backend/Dockerfile` installs `tesseract-ocr-eng` only; `tesseract-ocr-tel` and `tesseract-ocr-hin` must be installed in the container for Telugu/Hindi OCR to execute instead of falling back to English.
- **No Translation Endpoint**: `OpenAIProvider.translate()` is implemented in the provider class, but no REST endpoint currently exposes on-demand translation of `CriterionResult` or `ChangeEvent` summaries.

---

## Related Documentation

- [AI Assistant](../02-product/AI_ASSISTANT.md)
- [Document Processing](../03-architecture/DOCUMENT_PROCESSING.md)
- [Known Limitations](../08-testing-and-quality/KNOWN_LIMITATIONS.md)

