
from sympy import Matrix, latex, eye, Integer


def make_step(description, matrix, operation=None):
    return {
        "description": description,
        "operation": operation,
        "latex": latex(matrix),
    }


def eliminate(A: Matrix, reduced=False):
    """
    Gaussian / Gauss-Jordan elimination.

    reduced=False -> REF
    reduced=True  -> RREF

    All arithmetic remains exact.
    """
    M = A.copy()
    steps = [make_step("Original matrix", M)]

    pivot_row = 0
    pivots = []
    swaps = 0
    pivot_product = Integer(1)

    for col in range(M.cols):
        if pivot_row >= M.rows:
            break

        candidate = next(
            (
                row
                for row in range(pivot_row, M.rows)
                if M[row, col] != 0
            ),
            None,
        )

        if candidate is None:
            continue

        if candidate != pivot_row:
            M.row_swap(candidate, pivot_row)
            swaps += 1

            steps.append(
                make_step(
                    f"Swap R{candidate + 1} and R{pivot_row + 1}",
                    M,
                    "swap",
                )
            )

        pivot = M[pivot_row, col]
        pivot_product *= pivot

        if reduced and pivot != 1:
            M.row_op(
                pivot_row,
                lambda value, j: value / pivot,
            )

            steps.append(
                make_step(
                    f"Divide R{pivot_row + 1} by {pivot}",
                    M,
                    "scale",
                )
            )

        targets = (
            range(M.rows)
            if reduced
            else range(pivot_row + 1, M.rows)
        )

        for row in targets:
            if row == pivot_row:
                continue

            factor = M[row, col]

            if reduced:
                factor = factor / M[pivot_row, col]
            else:
                factor = factor / pivot

            if factor == 0:
                continue

            M.row_op(
                row,
                lambda value, j: (
                    value - factor * M[pivot_row, j]
                ),
            )

            steps.append(
                make_step(
                    f"R{row + 1} = R{row + 1} - "
                    f"({factor}) R{pivot_row + 1}",
                    M,
                    "eliminate",
                )
            )

        pivots.append(col)
        pivot_row += 1

    steps.append(
        make_step(
            "Final RREF" if reduced else "Final REF",
            M,
            "result",
        )
    )

    return {
        "matrix": M,
        "steps": steps,
        "pivots": pivots,
        "swaps": swaps,
        "pivot_product": pivot_product,
    }


def inverse_with_steps(A: Matrix):
    if not A.is_square:
        raise ValueError(
            "Inverse requires a square matrix."
        )

    n = A.rows

    augmented = A.row_join(eye(n))
    result = eliminate(augmented, reduced=True)

    left = result["matrix"][:, :n]
    right = result["matrix"][:, n:]

    if left != eye(n):
        raise ValueError(
            "Matrix is singular; no inverse exists."
        )

    if A * right != eye(n):
        raise ArithmeticError(
            "Inverse verification failed."
        )

    steps = [
        {
            "description": (
                "Augment matrix A with the identity matrix"
            ),
            "operation": "augment",
            "latex": latex(augmented),
        }
    ]

    steps.extend(result["steps"][1:])

    steps.append(
        make_step(
            "Extract inverse from the right-hand block",
            right,
            "result",
        )
    )

    return {
        "matrix": right,
        "steps": steps,
    }


def determinant_with_steps(A: Matrix):
    if not A.is_square:
        raise ValueError(
            "Determinant requires a square matrix."
        )

    result = eliminate(A, reduced=False)

    U = result["matrix"]
    swaps = result["swaps"]

    determinant = (
        (-1) ** swaps
        * result["pivot_product"]
    )

    if len(result["pivots"]) < A.rows:
        determinant = Integer(0)

    
    steps = result["steps"]

    if len(result["pivots"]) < A.rows:
        explanation = (
            "The matrix has fewer pivots than rows, "
            "so its determinant is zero."
        )
        formula = r"\det(A)=0"
    else:
        explanation = (
            "Multiply elimination pivots and apply "
            f"the sign from {swaps} row swaps."
        )
        formula = (
            r"\det(A)=(-1)^{"
            + str(swaps)
            + r"}\cdot"
            + latex(result["pivot_product"])
            + "="
            + latex(determinant)
        )

    steps.append({
        "description": explanation,
        "operation": "determinant",
        "latex": formula,
    })

    return {
        "value": determinant,
        "steps": steps,
    }
