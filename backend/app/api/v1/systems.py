
from fastapi import APIRouter, HTTPException

from app.schemas.linear_system import LinearSystemRequest
from app.services.linear_system_service import solve_system

router = APIRouter(
    prefix="/systems",
    tags=["Linear Systems"],
)


@router.post("/solve")
def solve_system_endpoint(question: LinearSystemRequest):
    try:
        return solve_system(question)

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
