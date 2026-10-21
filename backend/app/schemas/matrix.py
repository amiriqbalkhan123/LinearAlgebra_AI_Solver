
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class MatrixRequest(BaseModel):
    matrix: list[list[int]] = Field(min_length=1, max_length=10)
    operation: Literal[
        "determinant", "rank", "rref", "transpose"
    ]

    @model_validator(mode="after")
    def validate_matrix(self):
        width = len(self.matrix[0])

        if width < 1 or width > 10:
            raise ValueError("Matrix must have 1–10 columns.")

        if any(len(row) != width for row in self.matrix):
            raise ValueError("All rows must have equal length.")

        if any(
            abs(value) > 1_000_000
            for row in self.matrix
            for value in row
        ):
            raise ValueError("Matrix entries are too large.")

        return self
