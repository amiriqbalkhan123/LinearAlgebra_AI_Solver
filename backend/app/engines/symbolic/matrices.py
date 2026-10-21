
from sympy import Matrix, Rational, latex

from app.engines.step_by_step.elimination import (
    eliminate,
    inverse_with_steps,
    determinant_with_steps,
)


def parse_value(value: str):
    value = value.strip()

    if "/" in value:
        numerator, denominator = value.split("/")
        num = Rational(numerator)
        den = Rational(denominator)

        if den == 0:
            raise ValueError("Division by zero is not allowed.")

        result = num / den
    else:
        result = Rational(value)

    if abs(result.p) > 1_000_000 or result.q > 1_000_000:
        raise ValueError(
            "Matrix value exceeds supported numeric limits."
        )

    return result


def make_matrix(data):
    return Matrix([
        [parse_value(value) for value in row]
        for row in data
    ])


def calculate_matrix(matrix_data, operation, matrix_b=None):
    A = make_matrix(matrix_data)
    B = make_matrix(matrix_b) if matrix_b is not None else None

    steps = []
    verified = False

    if operation == "addition":
        if B is None or A.shape != B.shape:
            raise ValueError("Matrix dimensions must match.")
        result = A + B

    elif operation == "subtraction":
        if B is None or A.shape != B.shape:
            raise ValueError("Matrix dimensions must match.")
        result = A - B

    elif operation == "multiplication":
        if B is None or A.cols != B.rows:
            raise ValueError(
                "Columns of A must equal rows of B."
            )
        result = A * B

    elif operation == "determinant":
        output = determinant_with_steps(A)
        result = output["value"]
        steps = output["steps"]
        verified = result == A.det()

    elif operation == "inverse":
        output = inverse_with_steps(A)
        result = output["matrix"]
        steps = output["steps"]
        verified = A * result == Matrix.eye(A.rows)

    elif operation == "transpose":
        result = A.T

    elif operation == "rank":
        result = A.rank()

    elif operation == "ref":
        output = eliminate(A, reduced=False)
        result = output["matrix"]
        steps = output["steps"]
        verified = (
            result.is_echelon
            and result.rank() == A.rank()
        )

    elif operation == "rref":
        output = eliminate(A, reduced=True)
        result = output["matrix"]
        steps = output["steps"]
        verified = result == A.rref()[0]

    else:
        raise ValueError("Unsupported matrix operation.")

    if steps and not verified:
        raise ArithmeticError(
            "Mathematical verification failed."
        )

    return {
        "operation": operation,
        "input_latex": latex(A),
        "matrix_b_latex": latex(B) if B is not None else None,
        "result": str(result),
        "result_latex": latex(result),
        "steps": steps,
        "verified": verified,
    }
