
from app.engines.symbolic.eigenanalysis import analyze_eigen
from app.schemas.eigenanalysis import EigenanalysisRequest


def solve_eigenanalysis(question: EigenanalysisRequest):
    return analyze_eigen(question.matrix)
