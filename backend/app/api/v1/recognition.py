
from typing import Literal

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from app.ai.ocr.image_processor import load_image
from app.ai.ocr.recognizer import (
    OCRUnavailableError,
    recognize_text,
    recognize_formula,
)
from app.schemas.recognition import RecognitionResponse


router = APIRouter(
    prefix="/recognition",
    tags=["Image Recognition"],
)

MAX_UPLOAD_BYTES = 5 * 1024 * 1024

ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


@router.post(
    "/recognize",
    response_model=RecognitionResponse,
)
async def recognize_image(
    file: UploadFile = File(...),
    mode: Literal["text", "formula"] = Form("text"),
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Only PNG, JPEG and WEBP images are supported.",
        )

    try:
        data = await file.read(MAX_UPLOAD_BYTES + 1)
    finally:
        await file.close()

    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Image must be smaller than 5 MB.",
        )

    if not data:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty.",
        )

    try:
        image = load_image(data)

        if mode == "formula":
            latex_text = recognize_formula(image)

            return RecognitionResponse(
                mode="formula",
                recognized_text=latex_text,
                recognized_latex=latex_text or None,
                warning=(
                    "Verify the mathematical notation. "
                    "Recognition may contain errors."
                ),
            )

        text = recognize_text(image)

        return RecognitionResponse(
            mode="text",
            recognized_text=text,
            warning=(
                "Review the extracted text. "
                "Handwriting recognition may be inaccurate."
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except OCRUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )
