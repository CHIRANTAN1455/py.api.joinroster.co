"""
Image compression engine for profile photos and uploads.
Compresses images before saving to reduce storage and improve load times.
Laravel parity: store optimized images, not raw uploads.
"""
import io
from typing import Optional, Tuple

# Pillow is optional - if not installed, we skip compression
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Target max dimension (width or height) for profile photos
PROFILE_PHOTO_MAX_SIZE = 800
# JPEG quality (1-100)
JPEG_QUALITY = 85
# Max file size before we compress (bytes) - ~500KB
MAX_UNCOMPRESSED_BYTES = 512_000


def _get_output_format(mime_type: Optional[str], filename: str) -> str:
    """Determine output format from mime type or filename."""
    if mime_type:
        if "jpeg" in mime_type or "jpg" in mime_type:
            return "JPEG"
        if "png" in mime_type:
            return "PNG"
        if "webp" in mime_type:
            return "WEBP"
    ext = (filename or "").lower().split(".")[-1]
    if ext in ("jpg", "jpeg"):
        return "JPEG"
    if ext == "png":
        return "PNG"
    if ext == "webp":
        return "WEBP"
    return "JPEG"  # Default to JPEG for best compression


def compress_image(
    content: bytes,
    filename: str = "photo",
    mime_type: Optional[str] = None,
    max_size: int = PROFILE_PHOTO_MAX_SIZE,
    quality: int = JPEG_QUALITY,
) -> Tuple[bytes, str]:
    """
    Compress image content. Returns (compressed_bytes, extension).
    If Pillow is not available or image is invalid, returns original content.
    """
    if not HAS_PIL:
        ext = (filename or "photo").split(".")[-1] if "." in (filename or "") else "jpg"
        return content, ext if ext in ("jpg", "jpeg", "png", "webp") else "jpg"

    try:
        img = Image.open(io.BytesIO(content))
        # Convert RGBA to RGB for JPEG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        out_format = _get_output_format(mime_type, filename)
        if out_format == "PNG":
            # PNG doesn't use quality; use optimize
            out_format = "JPEG"
            img = img.convert("RGB")

        w, h = img.size
        if w > max_size or h > max_size:
            ratio = min(max_size / w, max_size / h)
            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format=out_format, quality=quality, optimize=True)
        compressed = buf.getvalue()

        # Only use compressed if it's actually smaller
        if len(compressed) < len(content) or len(content) > MAX_UNCOMPRESSED_BYTES:
            ext = "jpg" if out_format == "JPEG" else out_format.lower()
            return compressed, ext

        ext = (filename or "photo").split(".")[-1] if "." in (filename or "") else "jpg"
        return content, ext if ext in ("jpg", "jpeg", "png", "webp") else "jpg"
    except Exception:
        ext = (filename or "photo").split(".")[-1] if "." in (filename or "") else "jpg"
        return content, ext if ext in ("jpg", "jpeg", "png", "webp") else "jpg"
