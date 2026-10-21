
from typing import Any, Literal

from pydantic import BaseModel, Field


ProblemDomain = Literal[
    "matrices",
    "linear_systems",
    "vector_spaces",
    "vector_geometry",
    "eigenanalysis",
    "decompositions",
]


class UnifiedProblemRequest(BaseModel):
    domain: ProblemDomain

    data: dict[str, Any] = Field(
        description="Existing solver request payload."
    )


class UnifiedProblemResponse(BaseModel):
    domain: ProblemDomain
    status: Literal["success"]
    verified: bool
    result: dict[str, Any]
