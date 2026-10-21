
from fastapi import APIRouter, HTTPException

from app.schemas.decomposition import DecompositionRequest
from app.services.decomposition_service import solve_decomposition

router = APIRouter(
    prefix="/decompositions",
    tags=["Matrix Decompositions"],
)


@router.post("/analyze")
def analyze_endpoint(question: DecompositionRequest):
    try:
        return solve_decomposition(question)

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
