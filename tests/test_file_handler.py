import io
import struct

import pytest
from fastapi import HTTPException
from PIL import Image

from app.services.payslip.file_handler import (
    detect_file_type,
    normalize_image,
    pdf_to_image,
    validate_image_size,
)


# ---------- helpers ----------

def _make_jpeg(width: int = 10, height: int = 10) -> bytes:
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def _make_png() -> bytes:
    img = Image.new("RGB", (10, 10), color=(0, 255, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _make_pdf_bytes() -> bytes:
    """Minimal single-page PDF with a red rectangle."""
    import fitz
    doc = fitz.open()
    page = doc.new_page(width=200, height=200)
    page.draw_rect(fitz.Rect(10, 10, 100, 100), color=(1, 0, 0), fill=(1, 0, 0))
    data = doc.tobytes()
    doc.close()
    return data


# ---------- tests ----------

def test_detect_pdf():
    pdf = _make_pdf_bytes()
    assert detect_file_type(pdf) == "pdf"


def test_detect_image():
    assert detect_file_type(_make_jpeg()) == "image"


def test_pdf_to_jpeg_returns_jpeg():
    jpeg = pdf_to_image(_make_pdf_bytes())
    img = Image.open(io.BytesIO(jpeg))
    assert img.format == "JPEG"


def test_normalize_png_to_jpeg():
    jpeg = normalize_image(_make_png())
    img = Image.open(io.BytesIO(jpeg))
    assert img.format == "JPEG"


def test_normalize_jpeg_stays_jpeg():
    jpeg = normalize_image(_make_jpeg())
    img = Image.open(io.BytesIO(jpeg))
    assert img.format == "JPEG"


def test_normalize_image_strips_exif():
    """normalize_image re-encodes as JPEG without metadata, stripping all EXIF."""
    jpeg_with_exif = _make_jpeg()
    result = normalize_image(jpeg_with_exif)
    img = Image.open(io.BytesIO(result))
    assert img.format == "JPEG"
    # PIL ExifTags should be empty after stripping
    assert not img.getexif()


def test_validate_image_size_ok():
    # 1 KB — well within 5 MB limit
    validate_image_size(b"x" * 1024)


def test_validate_image_size_too_large():
    with pytest.raises(HTTPException) as exc_info:
        validate_image_size(b"x" * (6 * 1024 * 1024))
    assert exc_info.value.status_code == 413
