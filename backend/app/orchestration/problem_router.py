
from pydantic import ValidationError

from app.orchestration.operation_registry import SOLVER_REGISTRY
from app.schemas.problem import UnifiedProblemRequest


class InvalidProblemError(Exception):
    def __init__(self, details):
        self.details = details
        super().__init__("Invalid mathematical problem")


def route_problem(problem: UnifiedProblemRequest):
    schema_class, solver = SOLVER_REGISTRY[problem.domain]

    try:
        validated = schema_class.model_validate(problem.data)
    except ValidationError as error:
        raise InvalidProblemError(
            error.errors(include_context=False, include_url=False)
        ) from error

    result = solver(validated)

    if not isinstance(result, dict):
        raise ArithmeticError(
            "Solver returned an unexpected response."
        )

    return {
        "domain": problem.domain,
        "status": "success",
        "verified": result.get("verified", False) is True,
        "result": result,
    }
