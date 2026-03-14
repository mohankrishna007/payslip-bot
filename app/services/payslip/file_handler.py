import io
from typing import Literal

import filetype
import fitz  # PyMuPDF
from fastapi import HTTPException
from PIL import Image


def detect_file_type(data: bytes) -> Literal["image", "pdf"]:
    """Detect whether bytes represent a PDF or an image.

    Uses the filetype library to inspect the file signature (magic bytes)
    rather than only checking the first 4 bytes, covering edge cases like
    linearised PDFs and non-standard headers.
    """
    kind = filetype.guess(data)
    if kind is not None and kind.mime == "application/pdf":
        return "pdf"
    return "image"


def pdf_to_image(data: bytes) -> bytes:
    """Convert page 1 of a PDF to a JPEG byte string using PyMuPDF."""
    doc = fitz.open(stream=data, filetype="pdf")
    page = doc[0]
    pix = page.get_pixmap(dpi=100)  # 100 DPI is sufficient; 150 produced oversized images
    jpeg_bytes = pix.tobytes("jpeg")
    doc.close()
    return jpeg_bytes


def normalize_image(data: bytes) -> bytes:
    """Convert any PIL-readable image to JPEG bytes, stripping all EXIF metadata.

    Re-encoding via PIL without an explicit ``exif`` parameter drops all
    metadata (GPS, device info, etc.) automatically.
    """
    img = Image.open(io.BytesIO(data)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def compress_for_llm(data: bytes, max_dim: int = 800, quality: int = 75) -> bytes:
    """Resize to max_dim on longest side and re-encode at lower quality.

    Reduces a 2-3 MB salary slip to ~80-150 KB, cutting Gemini token usage
    by ~10x and staying well under the per-minute token quota.
    """
    img = Image.open(io.BytesIO(data)).convert("RGB")
    img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()


def validate_image_size(data: bytes, max_mb: float = 5.0) -> None:
    """Raise HTTP 413 if the image exceeds max_mb megabytes."""
    size_mb = len(data) / (1024 * 1024)
    if size_mb > max_mb:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.1f} MB). Maximum allowed size is {max_mb} MB.",
        )
