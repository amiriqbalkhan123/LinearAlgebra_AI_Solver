
from sympy import Matrix, Symbol, latex, simplify, zeros

from app.engines.symbolic.matrices import (
    make_matrix,
    parse_value,
)
from app.engines.step_by_step.elimination import eliminate


def solve_linear_system(matrix_data, constants_data):
    A = make_matrix(matrix_data)
    b = Matrix([
        parse_value(value)
        for value in constants_data
    ])

    augmented = A.row_join(b)

    # Use the Phase 3 elimination engine.
    # RREF includes a possible pivot in the final
    # augmented column for inconsistent systems.
    elimination = eliminate(augmented, reduced=True)
    R = elimination["matrix"]

    rank_a = A.rank()
    rank_augmented = augmented.rank()
    n = A.cols

    steps = [
        {
            "description": "Represent the system as Ax = b",
            "operation": "system",
            "latex": (
                latex(A)
                + latex(Matrix([
                    Symbol(f"x_{i+1}")
                    for i in range(n)
                ]))
                + "="
                + latex(b)
            ),
        }
    ]

    steps.extend(elimination["steps"])

    steps.append({
        "description": (
            f"Compare ranks: rank(A) = {rank_a}, "
            f"rank([A|b]) = {rank_augmented}, "
            f"unknowns = {n}"
        ),
        "operation": "rank",
        "latex": (
            r"\operatorname{rank}(A)="
            + str(rank_a)
            + r",\quad"
            + r"\operatorname{rank}([A\mid b])="
            + str(rank_augmented)
        ),
    })

    if rank_a < rank_augmented:
        classification = "no_solution"
        solution = None
        free_variables = []
        verified = rank_a < rank_augmented

        steps.append({
            "description": (
                "The augmented matrix has higher rank. "
                "The system is inconsistent."
            ),
            "operation": "classification",
            "latex": r"\varnothing",
        })

    else:
        # In a consistent RREF, pivot columns
        # within A identify basic variables.
        pivot_columns = []

        for row_index in range(R.rows):
            for col_index in range(n):
                if R[row_index, col_index] != 0:
                    pivot_columns.append(col_index)
                    break

        free_columns = [
            col for col in range(n)
            if col not in pivot_columns
        ]

        free_variables = [
            f"x_{col+1}" for col in free_columns
        ]

        # Parameters correspond exactly to
        # the free columns, in ascending order.
        parameters = {
            col: Symbol(f"t_{i+1}")
            for i, col in enumerate(free_columns)
        }

        x = zeros(n, 1)

        for col, parameter in parameters.items():
            x[col] = parameter

        for row_index, pivot_col in enumerate(pivot_columns):
            expression = R[row_index, n]

            for free_col in free_columns:
                expression -= (
                    R[row_index, free_col]
                    * x[free_col]
                )

            x[pivot_col] = simplify(expression)

        solution = x

        classification = (
            "unique"
            if rank_a == n
            else "infinite"
        )

        # Verify the complete parametric solution,
        # not just one sample assignment.
        verified = all(
            simplify(value) == 0
            for value in (A * x - b)
        )

        steps.append({
            "description": (
                "Express the variables in terms of "
                "free parameters."
                if classification == "infinite"
                else "Read the unique solution from RREF."
            ),
            "operation": "solution",
            "latex": (
                latex(Matrix([
                    Symbol(f"x_{i+1}")
                    for i in range(n)
                ]))
                + "="
                + latex(x)
            ),
        })

    if not verified:
        raise ArithmeticError(
            "Linear system verification failed."
        )

    return {
        "classification": classification,
        "rank_a": rank_a,
        "rank_augmented": rank_augmented,
        "unknowns": n,
        "equations": A.rows,
        "free_variables": free_variables,
        "input_latex": latex(augmented),
        "rref_latex": latex(R),
        "solution_latex": (
            latex(solution)
            if solution is not None
            else None
        ),
        "solution": (
            [str(value) for value in solution]
            if solution is not None
            else None
        ),
        "steps": steps,
        "verified": verified,
    }
