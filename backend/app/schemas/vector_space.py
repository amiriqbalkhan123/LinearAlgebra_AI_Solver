
from typing import Literal

from pydantic import BaseModel, model_validator
from app.schemas.matrix import validate_matrix


VectorSpaceOperation = Literal[
    "column_space",
    "row_space",
    "null_space",
    "left_null_space",
    "rank_nullity",
    "independence",
]


class VectorSpaceRequest(BaseModel):
    matrix: list[list[str]]
    operation: VectorSpaceOperation

    @model_validator(mode="after")
    def validate_input(self):
        validate_matrix(self.matrix, "A")
        return self
