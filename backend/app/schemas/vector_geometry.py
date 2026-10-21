
from typing import Literal

from pydantic import BaseModel, model_validator

from app.schemas.matrix import validate_matrix


VectorOperation = Literal[
    "addition",
    "subtraction",
    "scalar",
    "dot",
    "cross",
    "outer",
    "magnitude",
    "normalize",
    "distance",
    "angle",
    "orthogonality",
    "projection",
    "span_membership",
    "gram_schmidt",
]


BINARY = {
    "addition", "subtraction", "dot", "cross",
    "outer", "distance", "angle",
    "orthogonality", "projection",
}


class VectorGeometryRequest(BaseModel):
    operation: VectorOperation
    a: list[str] | None = None
    b: list[str] | None = None
    scalar: str | None = None
    vectors: list[list[str]] | None = None
    target: list[str] | None = None
    normalize_basis: bool = True

    @model_validator(mode="after")
    def validate_request(self):
        def check(v, name):
            if v is None:
                raise ValueError(f"{name} is required.")
            validate_matrix([v], name)

        if self.operation in BINARY:
            check(self.a, "a")
            check(self.b, "b")

        elif self.operation in {"magnitude", "normalize", "scalar"}:
            check(self.a, "a")

        elif self.operation in {"span_membership", "gram_schmidt"}:
            if not self.vectors or len(self.vectors) > 10:
                raise ValueError("Provide 1–10 vectors.")

            for vector in self.vectors:
                check(vector, "basis vector")

            length = len(self.vectors[0])

            if any(len(v) != length for v in self.vectors):
                raise ValueError(
                    "All vectors must have equal dimensions."
                )

            if self.operation == "span_membership":
                check(self.target, "target")

                if len(self.target) != length:
                    raise ValueError(
                        "Target and vectors must have the same dimension."
                    )

        if self.operation == "scalar":
            check([self.scalar] if self.scalar is not None else None, "scalar")

        if self.a is not None and self.b is not None:
            if self.operation in BINARY and len(self.a) != len(self.b):
                raise ValueError("Vector dimensions must match.")

        if self.operation == "cross" and len(self.a) != 3:
            raise ValueError("Cross product requires 3D vectors.")

        return self
