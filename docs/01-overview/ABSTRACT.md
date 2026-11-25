# Abstract

**NiyamDrishti** (*"Rule Vision"*) is an AI-powered government policy intelligence and personalized student opportunity platform designed to eliminate ambiguity in discovering, interpreting, and tracking government scholarships and welfare schemes across Andhra Pradesh, Telangana, and India.

Traditional scholarship portals function as static directories that force students to manually parse dense, multi-page official PDFs and leave them unaware when eligibility thresholds, financial benefits, or application deadlines change across academic cycles. Conversely, relying purely on generative AI for eligibility decisions introduces unacceptable hallucination risks.

NiyamDrishti resolves this tension through a **hybrid deterministic-AI architecture**:

1. **AI-Assisted Document Structuring**: Official notifications (PDF, DOCX, and scanned images) are validated (size, MIME allowlist, magic bytes, SHA-256), parsed via PyMuPDF and Tesseract OCR, and transformed by an abstracted LLM provider (`OpenAIProvider`) into Pydantic-validated JSONB rule conditions (`ExtractedSchemeRules`) anchored to verbatim `source_text` and `source_page` citations.
2. **Human-in-the-Loop Verification**: Extracted rules enter a reviewer queue (`review_status = "pending"`) and only govern live evaluations after explicit approval by authorized `document_reviewer` or `admin` users.
3. **Deterministic Eligibility Engine**: Student profiles are evaluated against approved rules using pure Python arithmetic and set logic (`EligibilityEngine`), producing transparent criterion-level outcomes (`passed`, `failed`, `unknown`), missing-field guidance, and directional match scores without LLM guessing.
4. **ChangeLens Policy Comparison**: A deterministic comparison engine (`PolicyComparisonEngine`) diffs two approved `SchemeVersion` snapshots to surface `added`, `removed`, and `modified` rules classified by severity (`high`, `medium`, `low`) with side-by-side evidence.
5. **Personalized Guidance (LifeMap & Multilingual Assistant)**: Approved evaluations connect to structured LifeMap action checklists, manual application status tracking, and a grounded multilingual assistant supporting English, Telugu, and Hindi.

Implemented with a **Next.js 16 / React 19 / Tailwind CSS v4** frontend, a **FastAPI / SQLAlchemy 2.0 async** backend, and **Supabase (PostgreSQL, Auth, Storage)**, NiyamDrishti establishes an auditable, privacy-respecting foundation for transparent public-scheme intelligence—while honestly documenting remaining integration work such as background worker execution, storage wiring, and RAG vector indexing.

---

## Related Documentation

- [Project Overview](PROJECT_OVERVIEW.md)
- [Problem Statement](PROBLEM_STATEMENT.md)
- [Key Innovations](KEY_INNOVATIONS.md)
- [Hackathon Overview](../11-hackathon/HACKATHON_OVERVIEW.md)

