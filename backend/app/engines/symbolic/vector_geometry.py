
from sympy import (
    Matrix, acos, latex, simplify, sqrt, eye
)

from app.engines.symbolic.matrices import parse_value


def vector(values):
    return Matrix([parse_value(x) for x in values])


def zero(expr):
    return simplify(expr) == 0


def solve_vector_geometry(question):
    op = question.operation
    a = vector(question.a) if question.a is not None else None
    b = vector(question.b) if question.b is not None else None

    steps = []
    verified = False

    def add_step(description, expression):
        steps.append({
            "description": description,
            "latex": latex(expression),
        })

    if op == "addition":
        result = a + b
        add_step("Add corresponding vector components.", result)
        verified = result - a == b

    elif op == "subtraction":
        result = a - b
        add_step("Subtract corresponding components.", result)
        verified = result + b == a

    elif op == "scalar":
        k = parse_value(question.scalar)
        result = k * a
        add_step("Multiply each component by the scalar.", result)
        verified = result == a * k

    elif op == "dot":
        result = a.dot(b)
        add_step("Multiply corresponding entries and sum.", result)
        verified = result == (a.T * b)[0]

    elif op == "cross":
        result = a.cross(b)
        add_step("Compute the three-dimensional cross product.", result)
        verified = zero(result.dot(a)) and zero(result.dot(b))

    elif op == "outer":
        result = a * b.T
        add_step("Multiply the column vector by the row vector.", result)
        verified = result.shape == (a.rows, b.rows)

    elif op == "magnitude":
        result = sqrt(a.dot(a))
        add_step("Find the square root of the sum of squares.", result)
        verified = zero(result**2 - a.dot(a))

    elif op == "normalize":
        norm = a.norm()

        if norm == 0:
            raise ValueError("Cannot normalize a zero vector.")

        result = a / norm
        add_step("Divide the vector by its magnitude.", result)
        verified = zero(result.dot(result) - 1)

    elif op == "distance":
        difference = a - b
        result = difference.norm()
        add_step("Calculate the difference vector.", difference)
        add_step("Calculate its Euclidean magnitude.", result)
        verified = zero(result**2 - difference.dot(difference))

    elif op == "angle":
        if a.norm() == 0 or b.norm() == 0:
            raise ValueError("Angle is undefined for a zero vector.")

        cosine = simplify(a.dot(b) / (a.norm() * b.norm()))
        result = acos(cosine)
        add_step("Calculate the cosine of the angle.", cosine)
        add_step("Apply inverse cosine (radians).", result)
        verified = zero(
            cosine * a.norm() * b.norm() - a.dot(b)
        )

    elif op == "orthogonality":
        dot = a.dot(b)
        result = dot == 0
        add_step("Check whether the dot product equals zero.", dot)
        verified = result == (a.T * b)[0].equals(0)

    elif op == "projection":
        denominator = b.dot(b)

        if denominator == 0:
            raise ValueError("Cannot project onto a zero vector.")

        coefficient = a.dot(b) / denominator
        result = coefficient * b

        add_step("Calculate the projection coefficient.", coefficient)
        add_step("Multiply by the direction vector.", result)

        verified = zero((a - result).dot(b))

    elif op == "span_membership":
        vectors = [vector(v) for v in question.vectors]
        target = vector(question.target)

        A = Matrix.hstack(*vectors)

        rank_a = A.rank()
        rank_augmented = A.row_join(target).rank()

        result = rank_a == rank_augmented

        add_step("Construct the matrix from the given vectors.", A)
        add_step("Calculate the rank of the vector matrix.", rank_a)
        add_step("Calculate the augmented matrix rank.", rank_augmented)

        if result:
            coefficients, parameters = A.gauss_jordan_solve(target)
            add_step("Find coefficients for a linear combination.", coefficients)
            verified = A * coefficients == target
        else:
            verified = rank_augmented > rank_a

    elif op == "gram_schmidt":
        vectors = [vector(v) for v in question.vectors]
        orthogonal = []

        for original in vectors:
            w = original.copy()

            for u in orthogonal:
                w -= (w.dot(u) / u.dot(u)) * u

            w = w.applyfunc(simplify)

            add_step("Remove projections onto previous vectors.", w)

            if any(not zero(value) for value in w):
                orthogonal.append(w)

        if question.normalize_basis:
            result = [u / u.norm() for u in orthogonal]
        else:
            result = orthogonal

        result = [
            u.applyfunc(simplify)
            for u in result
        ]

        for u in result:
            add_step("Resulting basis vector.", u)

        original_matrix = Matrix.hstack(*vectors)
        output_matrix = (
            Matrix.hstack(*result)
            if result else Matrix.zeros(vectors[0].rows, 0)
        )

        verified = (
            len(result) == original_matrix.rank()
            and output_matrix.rank() == original_matrix.rank()
            and all(
                zero(result[i].dot(result[j]))
                for i in range(len(result))
                for j in range(i + 1, len(result))
            )
            and (
                not question.normalize_basis
                or all(zero(u.dot(u) - 1) for u in result)
            )
        )

    else:
        raise ValueError("Unsupported vector operation.")

    if not verified:
        raise ArithmeticError("Vector verification failed.")

    if isinstance(result, list):
        result_latex = (
            r"\left\{"
            + ",".join(latex(v) for v in result)
            + r"\right\}"
        )
        result_text = [str(v) for v in result]

    elif isinstance(result, bool):
        result_latex = r"\mathrm{True}" if result else r"\mathrm{False}"
        result_text = result

    else:
        result_latex = latex(result)
        result_text = str(result)

    return {
        "operation": op,
        "result": result_text,
        "result_latex": result_latex,
        "steps": steps,
        "verified": verified,
    }
