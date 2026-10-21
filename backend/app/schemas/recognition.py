
from typing import Literal

from pydantic import BaseModel


class RecognitionResponse(BaseModel):
    mode: Literal["text", "formula"]
    recognized_text: str
    recognized_latex: str | None = None
    requires_confirmation: bool = True
    warning: str
