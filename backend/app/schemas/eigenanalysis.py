
from pydantic import BaseModel, model_validator

from app.schemas.matrix import validate_matrix


class EigenanalysisRequest(BaseModel):
    matrix: list[list[str]]

    @model_validator(mode="after")
    def validate_input(self):
        validate_matrix(self.matrix, "A")

        rows = len(self.matrix)
        cols = len(self.matrix[0])

        if rows != cols:
            raise ValueError(
                "Eigenanalysis requires a square matrix."
            )

        if rows > 4:
            raise ValueError(
                "Exact eigenanalysis currently supports "
                "matrices up to 4x4."
            )

        return self
