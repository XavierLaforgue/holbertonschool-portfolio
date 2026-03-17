from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile


MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]


def validate_image_file_size(value: UploadedFile) -> None:
    """Reject uploads larger than MAX_IMAGE_SIZE_MB."""
    if value.size > MAX_IMAGE_SIZE_BYTES:
        raise ValidationError(
            f"Image file size must not exceed {MAX_IMAGE_SIZE_MB} MB."
        )


def validate_image_file_type(value: UploadedFile) -> None:
    """Accept only JPEG, PNG, and WebP. Verified with Pillow."""
    from PIL import Image  # Python Imaging Library

    try:
        img = Image.open(value)
        img.verify()  # detect corrupt files without loading full data
    except Exception:
        raise ValidationError("Upload a valid image file.")

    # Map Pillow format names to MIME types
    pillow_to_mime = {  # MIME: Multipurpose Internet Mail Extensions
        "JPEG": "image/jpeg",
        "PNG": "image/png",
        "WEBP": "image/webp",
    }
    fmt: str = img.format or ""
    mime = pillow_to_mime.get(fmt)
    if mime not in ALLOWED_IMAGE_TYPES:
        allowed = ", ".join(
            mime_type.split("/")[1].upper()
            for mime_type in ALLOWED_IMAGE_TYPES
        )
        raise ValidationError(
            f"Unsupported image format '{img.format}'. "
            f"Allowed formats: {allowed}."
        )

    # Reset file pointer so it may be re-read
    value.seek(0)
