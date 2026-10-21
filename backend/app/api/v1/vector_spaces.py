
from fastapi import APIRouter, HTTPException

from app.schemas.vector_space import VectorSpaceRequest
from app.services.vector_space_service import solve_space

router = APIRouter(
    prefix="/vector-spaces",
    tags=["Vector Spaces"],
)


@router.post("/solve")
def solve_space_endpoint(question: VectorSpaceRequest):
    try:
        return solve_space(question)

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
