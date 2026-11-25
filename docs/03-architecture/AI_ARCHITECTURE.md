# AI Architecture

## Short Explanation

NiyamDrishti isolates all LLM usage behind an abstract `AIProvider` interface so generative models handle **unstructured text extraction, chat, and translation**, while deterministic Python engines retain sole authority over eligibility and policy comparison logic.

---

## 1. Why This Architecture Exists & What Problem It Solves

Coupling business logic directly to a single vendor SDK creates vendor lock-in and encourages mixing probabilistic text generation with deterministic eligibility checks. The `app/ai/` package separates provider APIs, Pydantic extraction schemas, and prompt-injection defenses.

---

## 2. AI Subsystem Diagram

```mermaid
flowchart LR
    subgraph Schemas["app/ai/schemas/extraction.py"]
        ESR["ExtractedSchemeRules"]
        ER["ExtractedRule"]
        CV["ConditionValue + RuleOperator + RuleCategory"]
    end

    subgraph Providers["app/ai/providers/"]
        BASE["AIProvider (ABC: extract_structured, chat, translate)"]
        OAI["OpenAIProvider (Implemented)"]
        ANT["AnthropicProvider (Planned — not yet implemented)"]
    end

    subgraph Consumers["Backend Consumers"]
        AST["assistant/router.py (POST /api/v1/assistant/chat)"]
        EXT["Future Worker (extract_rules job)"]
    end

    AST --> OAI
    EXT -.-> BASE
    BASE <|-- OAI
    BASE <|.. ANT
    OAI --> Schemas
    OAI --> OPENAI["OpenAI API (gpt-4o / gpt-4o-mini)"]
```

---

## 3. Technical Implementation

### Abstract Interface (`backend/app/ai/providers/base.py`)

Defines three async methods on `AIProvider`:
1. `extract_structured(text, schema, system_prompt, model=None) -> BaseModel`
2. `chat(messages, system_prompt, model=None, temperature=0.3) -> str`
3. `translate(text, target_language, context=None) -> str`

### OpenAI Implementation (`backend/app/ai/providers/openai_provider.py`)

- Uses `openai.AsyncOpenAI(api_key=settings.openai_api_key)`.
- **`extract_structured`**:
  - Defaults to `settings.openai_extraction_model` (`gpt-4o`).
  - Wraps document text in `<document>\n{text[:50000]}\n</document>` and appends an anti-injection system instruction.
  - Calls `self.client.beta.chat.completions.parse(..., response_format=schema, temperature=0)` to enforce Pydantic schema conformance.
- **`chat`**:
  - Defaults to `settings.openai_model` (`gpt-4o-mini`), `temperature=0.3`, `max_tokens=2000`.
- **`translate`**:
  - Maps `te` → Telugu, `hi` → Hindi, `en` → English (`temperature=0.1`) while preserving scheme/institution proper nouns.

### Extraction Schemas (`backend/app/ai/schemas/extraction.py`)

- `RuleOperator`: `lte`, `lt`, `gte`, `gt`, `eq`, `neq`, `in`, `not_in`, `any`
- `RuleCategory`: `income`, `marks`, `cgpa`, `age`, `category`, `disability`, `domicile`, `state`, `course`, `education_level`, `amount`, `deadline`, `document`, `renewal`, `exclusion`, `other`
- `ConditionValue`: Recursive Pydantic model supporting `sub_conditions` and `logic` (`and`/`or`).
- `ExtractedRule` & `ExtractedSchemeRules`: Include `source_text`, `source_page`, `confidence` (`0.0–1.0`), `required_documents`, `application_procedure`, and `renewal_conditions`.

---

## 4. Current Implementation Status & Gaps

- **Implemented**: `AIProvider` ABC, `OpenAIProvider` (all 3 methods), `ExtractedSchemeRules` schema, and `assistant/router.py` chat usage.
- **Not Yet Implemented**:
  - `AnthropicProvider` (even though `anthropic==0.40.0` is in `requirements.txt` and `anthropic_api_key` is in `config.py`).
  - Wiring `OpenAIProvider.extract_structured()` into a background document processing worker.
  - Vector embeddings / pgvector / RAG retrieval for `assistant/chat` citations.

---

## 5. Related Documentation

- [AI Overview](../06-ai-and-intelligence/AI_OVERVIEW.md)
- [Rule Extraction](../06-ai-and-intelligence/RULE_EXTRACTION.md)
- [Document Processing](DOCUMENT_PROCESSING.md)
- [Multilingual Support](../06-ai-and-intelligence/MULTILINGUAL_SUPPORT.md)

