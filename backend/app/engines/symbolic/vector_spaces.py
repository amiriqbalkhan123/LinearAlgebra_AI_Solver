
from sympy import latex, zeros

from app.engines.symbolic.matrices import make_matrix
from app.engines.step_by_step.elimination import eliminate


def solve_vector_space(matrix_data, operation):
    A = make_matrix(matrix_data)

    rref_data = eliminate(A, reduced=True)
    R = rref_data["matrix"]
    pivots = rref_data["pivots"]

    rank = len(pivots)
    nullity = A.cols - rank

    column_basis = [A.col(i) for i in pivots]
    row_basis = [
        R.row(i).T
        for i in range(rank)
    ]
    null_basis = A.nullspace()
    left_null_basis = A.T.nullspace()

    is_independent = rank == A.cols

    operations = {
        "column_space": (
            "Column Space",
            column_basis,
            A.rows,
        ),
        "row_space": (
            "Row Space",
            row_basis,
            A.cols,
        ),
        "null_space": (
            "Null Space",
            null_basis,
            A.cols,
        ),
        "left_null_space": (
            "Left Null Space",
            left_null_basis,
            A.rows,
        ),
    }

    basis = []
    ambient_dimension = None

    if operation in operations:
        name, basis, ambient_dimension = operations[operation]
        dimension = len(basis)

    elif operation == "rank_nullity":
        name = "Rank–Nullity Theorem"
        dimension = None

    elif operation == "independence":
        name = "Linear Independence"
        dimension = rank

    else:
        raise ValueError("Unsupported vector-space operation.")

    # Independent mathematical consistency checks.
    verified = (
        rank == A.rank()
        and rank + nullity == A.cols
        and len(column_basis) == rank
        and len(row_basis) == rank
        and len(null_basis) == nullity
        and len(left_null_basis) == A.rows - rank
        and all(A * v == zeros(A.rows, 1) for v in null_basis)
        and all(
            A.T * v == zeros(A.cols, 1)
            for v in left_null_basis
        )
        and all(
            R * v == zeros(A.rows, 1)
            for v in null_basis
        )
    )

    if not verified:
        raise ArithmeticError(
            "Vector-space verification failed."
        )

    steps = [
        {
            "description": "Original matrix",
            "latex": latex(A),
        },
    ]

    steps.extend({
        "description": step["description"],
        "latex": step["latex"],
    } for step in rref_data["steps"][1:])

    steps.append({
        "description": (
            f"Identify pivot columns "
            f"{[i + 1 for i in pivots]} and rank {rank}."
        ),
        "latex": (
            r"\operatorname{rank}(A)="
            + str(rank)
        ),
    })

    if operation == "rank_nullity":
        steps.append({
            "description": "Verify the rank–nullity theorem.",
            "latex": (
                str(rank)
                + "+"
                + str(nullity)
                + "="
                + str(A.cols)
            ),
        })

    elif operation == "independence":
        steps.append({
            "description": (
                "All columns are independent."
                if is_independent
                else "The columns are linearly dependent."
            ),
            "latex": (
                r"\operatorname{rank}(A)="
                + str(rank)
                + (r"=n" if is_independent else r"<n")
            ),
        })

    else:
        steps.append({
            "description": (
                f"Extract a basis for the {name.lower()}. "
                "The empty basis represents the zero subspace."
            ),
            "latex": (
                r"\left\{"
                + ",".join(latex(v) for v in basis)
                + r"\right\}"
            ),
        })

    return {
        "operation": operation,
        "name": name,
        "input_latex": latex(A),
        "rref_latex": latex(R),
        "pivot_columns": [i + 1 for i in pivots],
        "rank": rank,
        "nullity": nullity,
        "dimension": dimension,
        "ambient_dimension": ambient_dimension,
        "basis": [
            [str(value) for value in vector]
            for vector in basis
        ],
        "basis_latex": [latex(v) for v in basis],
        "is_independent": (
            is_independent
            if operation == "independence"
            else None
        ),
        "steps": steps,
        "verified": verified,
    }
