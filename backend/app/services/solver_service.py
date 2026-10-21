
from app.engines.symbolic.matrices import calculate_matrix
from app.schemas.matrix import MatrixRequest


def solve_matrix(question: MatrixRequest):
    return calculate_matrix(
        matrix_data=question.matrix,
        matrix_b=question.matrix_b,
        operation=question.operation,
    )
