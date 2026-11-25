# Backend Setup

## Short Explanation

The FastAPI backend requires Python 3.10+ (3.11 in Docker/CI) and optional system binaries (`tesseract-ocr`, `poppler-utils`) if you test scanned-PDF OCR locally.

---

## 1. Virtual Environment & Dependencies

```bash
cd backend
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If running unit tests with SQLite in-memory (like CI), also install `aiosqlite` if not already in your environment:

```bash
pip install aiosqlite
```

---

## 2. Running the API & Tests

```bash
# Start development server with hot reload
uvicorn app.main:app --reload --port 8000

# Run unit tests
pytest -v
```

---

## Related Documentation

- [Backend Architecture](../03-architecture/BACKEND_ARCHITECTURE.md)
- [Unit Testing](../08-testing-and-quality/UNIT_TESTING.md)
- [Render Deployment](../09-deployment-and-devops/RENDER_DEPLOYMENT.md)

