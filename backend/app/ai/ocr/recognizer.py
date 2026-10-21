
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



import base64
import json
import subprocess
from io import BytesIO
from pathlib import Path

from PIL import Image


def recognize_formula(image: Image.Image) -> str:
    backend_dir = Path(__file__).resolve().parents[3]

    python_executable = (
        backend_dir / ".venv-ocr" / "Scripts" / "python.exe"
    )

    worker_script = (
        backend_dir / "app" / "ai" / "ocr" / "formula_worker.py"
    )

    if not python_executable.is_file():
        raise OCRUnavailableError(
            "OCR Python environment not found: "
            f"{python_executable}"
        )

    if not worker_script.is_file():
        raise OCRUnavailableError(
            "Formula OCR worker script not found."
        )

    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="PNG")

    payload = json.dumps({
        "image": base64.b64encode(
            buffer.getvalue()
        ).decode("ascii"),
    })

    try:
        completed = subprocess.run(
            [str(python_executable), str(worker_script)],
            input=payload,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )

    except subprocess.TimeoutExpired as error:
        raise OCRUnavailableError(
            "Mathematical OCR exceeded the 120-second limit."
        ) from error

    except OSError as error:
        raise OCRUnavailableError(
            "Could not start the OCR worker."
        ) from error

    try:
        response = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise OCRUnavailableError(
            "OCR worker returned an invalid response."
        ) from error

    if completed.returncode != 0 or not response.get("success"):
        raise OCRUnavailableError(
            "Mathematical OCR failed. Check worker dependencies "
            "and model initialization."
        )

    return response["latex"]
