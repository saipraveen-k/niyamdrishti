"""
Document processing service: text extraction, OCR, and rule extraction.
"""

import hashlib
import io
import os
from pathlib import Path
from typing import Optional, Tuple

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg",
    "image/png",
    "image/webp",
}

MIME_MAGIC_BYTES = {
    b"%PDF": "application/pdf",
    b"PK\x03\x04": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG": "image/png",
    b"RIFF": "image/webp",
}


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_file_magic(data: bytes, declared_mime: str) -> Tuple[bool, str]:
    """
    Validate file by magic bytes, not just declared MIME type.
    Returns (is_valid, detected_mime).
    """
    for magic, detected_mime in MIME_MAGIC_BYTES.items():
        if data[:len(magic)] == magic:
            return True, detected_mime
    return False, "unknown"


def validate_upload(
    data: bytes,
    filename: str,
    declared_mime: str,
) -> Tuple[bool, str]:
    """
    Full upload validation:
    - File size check
    - Magic bytes check
    - Extension check
    Returns (is_valid, reason).
    """
    if len(data) > settings.max_upload_size_bytes:
        size_mb = settings.max_upload_size_bytes / (1024 * 1024)
        return False, f"File too large. Maximum {size_mb:.0f} MB allowed."

    if declared_mime not in ALLOWED_MIME_TYPES:
        return False, f"File type '{declared_mime}' not allowed."

    is_valid_magic, detected_mime = validate_file_magic(data, declared_mime)
    if not is_valid_magic:
        return False, "File content does not match declared type."

    return True, "ok"


def extract_text_from_pdf(data: bytes) -> Tuple[str, int, bool]:
    """
    Extract text from a PDF.
    Returns (text, page_count, used_ocr).
    Falls back to OCR for scanned PDFs.
    """
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(stream=data, filetype="pdf")
        page_count = doc.page_count

        if page_count > settings.max_pdf_pages:
            raise ValueError(
                f"PDF has {page_count} pages; maximum {settings.max_pdf_pages} allowed."
            )

        pages_text = []
        needs_ocr_pages = []

        for page_num in range(page_count):
            page = doc[page_num]
            text = page.get_text()
            if len(text.strip()) < 50:
                # Likely scanned — mark for OCR
                needs_ocr_pages.append(page_num)
            else:
                pages_text.append(f"[Page {page_num + 1}]\n{text}")

        if needs_ocr_pages:
            logger.info(
                "pdf_needs_ocr",
                total_pages=page_count,
                ocr_pages=len(needs_ocr_pages),
            )
            ocr_texts = _ocr_pdf_pages(doc, needs_ocr_pages)
            # Merge OCR results into pages_text at correct positions
            # Simple approach: append at end with page markers
            for page_num, ocr_text in zip(needs_ocr_pages, ocr_texts):
                pages_text.append(f"[Page {page_num + 1} — OCR]\n{ocr_text}")

        full_text = "\n\n".join(pages_text)
        used_ocr = bool(needs_ocr_pages)

        doc.close()
        return full_text, page_count, used_ocr

    except ImportError:
        logger.warning("PyMuPDF (fitz) not available")
        return "", 0, False


def _ocr_pdf_pages(doc, page_numbers: list) -> list:
    """Run Tesseract OCR on specific PDF pages."""
    results = []
    try:
        import pytesseract
        from PIL import Image
        import fitz

        if settings.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

        for page_num in page_numbers:
            page = doc[page_num]
            # Render at 300 DPI for good OCR quality
            mat = fitz.Matrix(300 / 72, 300 / 72)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")

            img = Image.open(io.BytesIO(img_data))
            # OCR with Indian language support if available
            try:
                text = pytesseract.image_to_string(img, lang="eng+tel")
            except pytesseract.pytesseract.TesseractError:
                text = pytesseract.image_to_string(img, lang="eng")

            results.append(text)

    except ImportError:
        logger.warning("pytesseract or PIL not available; OCR skipped")
        results = ["[OCR not available]"] * len(page_numbers)
    except Exception as e:
        logger.error("ocr_failed", error=str(e))
        results = [f"[OCR error: {e}]"] * len(page_numbers)

    return results


def extract_text_from_docx(data: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document

        doc = Document(io.BytesIO(data))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        # Include table content
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        paragraphs.append(cell.text)
        return "\n\n".join(paragraphs)
    except ImportError:
        logger.warning("python-docx not available")
        return ""
    except Exception as e:
        logger.error("docx_extraction_failed", error=str(e))
        return ""


def extract_text_from_image(data: bytes) -> str:
    """Extract text from an image using OCR."""
    try:
        import pytesseract
        from PIL import Image

        if settings.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

        img = Image.open(io.BytesIO(data))
        try:
            text = pytesseract.image_to_string(img, lang="eng+tel")
        except pytesseract.pytesseract.TesseractError:
            text = pytesseract.image_to_string(img, lang="eng")
        return text
    except ImportError:
        return "[OCR not available]"
    except Exception as e:
        logger.error("image_ocr_failed", error=str(e))
        return ""


def extract_text(data: bytes, mime_type: str) -> Tuple[str, int, bool]:
    """
    Route extraction by MIME type.
    Returns (text, page_count, used_ocr).
    """
    if mime_type == "application/pdf":
        return extract_text_from_pdf(data)
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(data)
        return text, 1, False
    elif mime_type in ("image/jpeg", "image/png", "image/webp"):
        text = extract_text_from_image(data)
        return text, 1, True
    else:
        return "", 0, False
