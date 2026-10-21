
import re
from typing import Literal

from pydantic import BaseModel, Field, model_validator


MatrixOperation = Literal[
    "addition",
    "subtraction",
    "multiplication",
    "determinant",
    "inverse",
    "transpose",
    "rank",
    "rref",
]

NUMBER_PATTERN = re.compile(
    r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)"
    r"(?:/[+-]?\d+(?:\.\d*)?|\.\d+)?$"
)


def validate_matrix(matrix, name):
    if not matrix or len(matrix) > 10:
        raise ValueError(
            f"Matrix {name} must have 1–10 rows."
        )

    width = len(matrix[0])

    if width < 1 or width > 10:
        raise ValueError(
            f"Matrix {name} must have 1–10 columns."
        )

    for row in matrix:
        if len(row) != width:
            raise ValueError(
                f"Matrix {name} has inconsistent row lengths."
            )

        for value in row:
            if not NUMBER_PATTERN.fullmatch(value.strip()):
                raise ValueError(
                    f"Invalid matrix entry: {value}"
                )

            if len(value.strip()) > 30:
                raise ValueError("Matrix entry too long.")


class MatrixRequest(BaseModel):
    matrix: list[list[str]] = Field(min_length=1)
    matrix_b: list[list[str]] | None = None
    operation: MatrixOperation

    @model_validator(mode="after")
    def check_matrices(self):
        validate_matrix(self.matrix, "A")

        if self.matrix_b is not None:
            validate_matrix(self.matrix_b, "B")

        if self.operation in (
            "addition",
            "subtraction",
            "multiplication",
        ) and self.matrix_b is None:
            raise ValueError(
                "This operation requires matrix B."
            )

        return self
