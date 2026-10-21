
from app.schemas.vector_space import VectorSpaceRequest
from app.engines.symbolic.vector_spaces import solve_vector_space


def solve_space(question: VectorSpaceRequest):
    return solve_vector_space(
        question.matrix,
        question.operation,
    )
