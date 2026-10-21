
from fastapi import APIRouter, HTTPException

from app.schemas.vector_geometry import VectorGeometryRequest
from app.services.vector_geometry_service import solve_geometry

router = APIRouter(
    prefix="/vector-geometry",
    tags=["Vector Geometry"],
)


@router.post("/solve")
def solve_geometry_endpoint(question: VectorGeometryRequest):
    try:
        return solve_geometry(question)

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
