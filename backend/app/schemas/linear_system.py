
from pydantic import BaseModel, Field, model_validator

from app.schemas.matrix import validate_matrix


class LinearSystemRequest(BaseModel):
    matrix: list[list[str]] = Field(
        min_length=1,
        max_length=10,
    )
    constants: list[str] = Field(
        min_length=1,
        max_length=10,
    )

    @model_validator(mode="after")
    def validate_system(self):
        validate_matrix(self.matrix, "A")

        validate_matrix(
            [[value] for value in self.constants],
            "b",
        )

        if len(self.matrix) != len(self.constants):
            raise ValueError(
                "The number of constants must equal "
                "the number of equations."
            )

        return self
