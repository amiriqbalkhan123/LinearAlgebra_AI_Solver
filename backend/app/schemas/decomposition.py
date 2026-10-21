
from typing import Literal

from pydantic import BaseModel, model_validator
from app.schemas.matrix import validate_matrix


DecompositionOperation = Literal[
    "lu",
    "qr",
    "svd",
    "pseudoinverse",
    "least_squares",
    "spectral",
    "positive_definite",
]


class DecompositionRequest(BaseModel):
    matrix: list[list[str]]
    operation: DecompositionOperation
    constants: list[str] | None = None

    @model_validator(mode="after")
    def validate_request(self):
        validate_matrix(self.matrix, "A")

        rows = len(self.matrix)
        cols = len(self.matrix[0])

        if self.operation == "svd":
            limit = 10
        else:
            limit = 6

        if rows > limit or cols > limit:
            raise ValueError(
                f"This operation supports up to {limit}x{limit}."
            )

        if self.operation in {
            "spectral", "positive_definite"
        } and rows != cols:
            raise ValueError(
                "This operation requires a square matrix."
            )

        if self.operation == "least_squares":
            if self.constants is None:
                raise ValueError("Constants vector b is required.")

            validate_matrix(
                [[v] for v in self.constants],
                "b",
            )

            if len(self.constants) != rows:
                raise ValueError(
                    "Vector b must have one entry per row of A."
                )

        return self
