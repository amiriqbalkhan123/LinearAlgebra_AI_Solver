
from sympy import Matrix, latex


def calculate_matrix(matrix_data, operation):
    matrix = Matrix(matrix_data)

    if operation == "determinant":
        if not matrix.is_square:
            raise ValueError("Determinant requires a square matrix.")
        result = matrix.det()

    elif operation == "rank":
        result = matrix.rank()

    elif operation == "rref":
        result = matrix.rref()[0]

    elif operation == "transpose":
        result = matrix.T

    else:
        raise ValueError("Unsupported matrix operation.")

    return {
        "operation": operation,
        "input_latex": latex(matrix),
        "result": str(result),
        "result_latex": latex(result),
    }
