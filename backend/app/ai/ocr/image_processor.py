
from io import BytesIO

from PIL import (
    Image,
    ImageOps,
    ImageFilter,
    UnidentifiedImageError,
)

MAX_PIXELS = 16_000_000
Image.MAX_IMAGE_PIXELS = MAX_PIXELS


def load_image(data: bytes) -> Image.Image:
    try:
        image = Image.open(BytesIO(data))
        image.load()

        if image.format not in {"PNG", "JPEG", "WEBP"}:
            raise ValueError(
                "Only PNG, JPEG and WEBP images are supported."
            )

        if image.width * image.height > MAX_PIXELS:
            raise ValueError("Image dimensions are too large.")

        if image.width < 20 or image.height < 20:
            raise ValueError("Image resolution is too small.")

        return ImageOps.exif_transpose(image).convert("RGB")

    except (UnidentifiedImageError, OSError) as error:
        raise ValueError(
            "Invalid or corrupted image."
        ) from error


def prepare_text_image(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray)

    if max(gray.size) < 1500:
        gray = gray.resize(
            (gray.width * 2, gray.height * 2),
            Image.Resampling.LANCZOS,
        )

    return gray.filter(ImageFilter.SHARPEN)


def prepare_formula_image(image: Image.Image) -> Image.Image:
    return ImageOps.autocontrast(image.convert("RGB"))
