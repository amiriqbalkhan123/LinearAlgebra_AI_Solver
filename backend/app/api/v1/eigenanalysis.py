
from fastapi import APIRouter, HTTPException
from sympy.matrices.exceptions import MatrixError
from sympy.polys.polyerrors import PolynomialError

from app.schemas.eigenanalysis import EigenanalysisRequest
from app.services.eigenanalysis_service import solve_eigenanalysis


router = APIRouter(
    prefix="/eigenanalysis",
    tags=["Eigenanalysis"],
)


@router.post("/analyze")
def analyze_endpoint(question: EigenanalysisRequest):
    try:
        return solve_eigenanalysis(question)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except (MatrixError, PolynomialError, NotImplementedError):
        raise HTTPException(
            status_code=422,
            detail=(
                "Exact eigenanalysis could not be completed "
                "for this matrix."
            ),
        )

    except ArithmeticError:
        raise HTTPException(
            status_code=500,
            detail="Mathematical verification failed.",
        )
