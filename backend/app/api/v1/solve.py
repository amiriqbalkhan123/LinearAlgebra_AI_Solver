
from fastapi import APIRouter, HTTPException

from app.schemas.matrix import MatrixRequest
from app.services.solver_service import solve_matrix

router = APIRouter(
    prefix="/solve",
    tags=["Solver"],
)


@router.post("/matrix")
def solve_matrix_endpoint(question: MatrixRequest):
    try:
        return solve_matrix(question)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except ArithmeticError:
        raise HTTPException(
            status_code=500,
            detail="Mathematical verification failed.",
        )
