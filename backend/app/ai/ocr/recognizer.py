
from functools import lru_cache
from pathlib import Path
import shutil

import pytesseract
from pathlib import Path
import shutil

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if Path(TESSERACT_PATH).is_file():
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
else:
    pytesseract.pytesseract.tesseract_cmd = (
        shutil.which("tesseract") or "tesseract"
    )
    
from PIL import Image

from app.ai.ocr.image_processor import (
    prepare_text_image,
    prepare_formula_image,
)


class OCRUnavailableError(Exception):
    pass


def recognize_text(image: Image.Image) -> str:
    executable = shutil.which("tesseract")

    if executable is None:
        fallback = Path(
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )
        if fallback.is_file():
            executable = str(fallback)

    if executable is None:
        raise OCRUnavailableError(
            "Tesseract is not installed or not on PATH."
        )

    pytesseract.pytesseract.tesseract_cmd = executable

    prepared = prepare_text_image(image)

    try:
        return pytesseract.image_to_string(
            prepared,
            lang="eng",
            config="--psm 6",
            timeout=20,
        ).strip()

    except (RuntimeError, pytesseract.TesseractError) as error:
        raise OCRUnavailableError(
            f"Text OCR failed: {error}"
        ) from error


@lru_cache(maxsize=1)
def get_formula_model():
    try:
        from pix2tex.cli import LatexOCR
        return LatexOCR()
    except (ImportError, OSError, RuntimeError) as error:
        raise OCRUnavailableError(
            "pix2tex could not be initialized. "
            "Check its dependencies and model files."
        ) from error


def recognize_formula(image: Image.Image) -> str:
    model = get_formula_model()
    prepared = prepare_formula_image(image)

    try:
        return str(model(prepared)).strip()
    except (RuntimeError, ValueError) as error:
        raise OCRUnavailableError(
            "Mathematical OCR inference failed."
        ) from error
