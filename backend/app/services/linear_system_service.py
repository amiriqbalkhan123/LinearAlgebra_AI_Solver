
from app.schemas.linear_system import LinearSystemRequest
from app.engines.symbolic.linear_systems import solve_linear_system


def solve_system(question: LinearSystemRequest):
    return solve_linear_system(
        question.matrix,
        question.constants,
    )
