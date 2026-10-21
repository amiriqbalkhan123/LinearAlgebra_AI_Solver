
import logging

from fastapi import APIRouter, HTTPException

from app.schemas.problem import (
    UnifiedProblemRequest,
    UnifiedProblemResponse,
)

from app.orchestration.problem_router import (
    InvalidProblemError,
    route_problem,
)

router = APIRouter(
    prefix="/problems",
    tags=["Unified Problem Solver"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/solve",
    response_model=UnifiedProblemResponse,
)
def solve_problem(problem: UnifiedProblemRequest):
    try:
        return route_problem(problem)

    except InvalidProblemError as error:
        raise HTTPException(
            status_code=422,
            detail=error.details,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except (ArithmeticError, NotImplementedError):
        logger.exception("Problem solving failed")
        raise HTTPException(
            status_code=422,
            detail="The solver could not complete this problem.",
        )
