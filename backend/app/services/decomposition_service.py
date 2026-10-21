
from app.engines.symbolic.decompositions import analyze_decomposition
from app.schemas.decomposition import DecompositionRequest


def solve_decomposition(question: DecompositionRequest):
    return analyze_decomposition(question)
