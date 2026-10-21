
from sympy import (
    Matrix,
    Symbol,
    diag,
    factor,
    latex,
    simplify,
    zeros,
)

from app.engines.symbolic.matrices import make_matrix


def is_zero_matrix(matrix):
    return all(simplify(x) == 0 for x in matrix)


def analyze_eigen(matrix_data):
    A = make_matrix(matrix_data)
    n = A.rows
    lam = Symbol("lambda")

    if n != A.cols or n > 4:
        raise ValueError(
            "A square matrix of size 1 to 4 is required."
        )

    charpoly = A.charpoly(lam)
    polynomial = charpoly.as_expr()
    factored = factor(polynomial)

    steps = [
        {
            "description": "Start with the original matrix A.",
            "latex": rf"A={latex(A)}",
        },
        {
            "description": (
                "Construct the characteristic matrix."
            ),
            "latex": (
                rf"\lambda I-A="
                rf"{latex(lam * Matrix.eye(n) - A)}"
            ),
        },
        {
            "description": (
                "Calculate the characteristic polynomial."
            ),
            "latex": (
                rf"p_A(\lambda)="
                rf"\det(\lambda I-A)="
                rf"{latex(polynomial)}"
            ),
        },
        {
            "description": (
                "Factor the characteristic polynomial."
            ),
            "latex": (
                rf"p_A(\lambda)={latex(factored)}"
            ),
        },
    ]

    # Retrieve eigenvalues, multiplicities,
    # and independent eigenspace basis vectors.
    eigen_data = A.eigenvects()

    eigenvalues = []
    all_vectors = []
    diagonal_entries = []

    for eigenvalue, algebraic_mult, basis in eigen_data:
        geometric_mult = len(basis)

        shifted = A - eigenvalue * Matrix.eye(n)

        eigen_verified = (
            geometric_mult > 0
            and geometric_mult <= algebraic_mult
            and all(
                is_zero_matrix(shifted * v)
                for v in basis
            )
            and Matrix.hstack(*basis).rank()
            == geometric_mult
        )

        if not eigen_verified:
            raise ArithmeticError(
                "Eigenvector verification failed."
            )

        eigenvalues.append({
            "value": str(eigenvalue),
            "value_latex": latex(eigenvalue),
            "algebraic_multiplicity": algebraic_mult,
            "geometric_multiplicity": geometric_mult,
            "basis": [
                [str(x) for x in v]
                for v in basis
            ],
            "basis_latex": [
                latex(v) for v in basis
            ],
            "verified": True,
        })

        steps.append({
            "description": (
                f"For eigenvalue {eigenvalue}, "
                "solve (A - λI)v = 0."
            ),
            "latex": (
                rf"(A-({latex(eigenvalue)})I)v=0"
            ),
        })

        steps.append({
            "description": (
                "Find the eigenspace basis by "
                "reducing the shifted matrix."
            ),
            "latex": (
                rf"A-({latex(eigenvalue)})I="
                rf"{latex(shifted)}"
                rf"\longrightarrow"
                rf"{latex(shifted.rref()[0])}"
            ),
        })

        for v in basis:
            steps.append({
                "description": (
                    "Verify this eigenvector using Av = λv."
                ),
                "latex": (
                    rf"{latex(A)}{latex(v)}="
                    rf"{latex(eigenvalue)}{latex(v)}"
                ),
            })

            all_vectors.append(v)
            diagonal_entries.append(eigenvalue)

    if sum(
        e["algebraic_multiplicity"]
        for e in eigenvalues
    ) != n:
        raise ArithmeticError(
            "Incomplete eigenvalue multiplicities."
        )

    diagonalizable = len(all_vectors) == n

    P = None
    D = None

    if diagonalizable:
        P = Matrix.hstack(*all_vectors)
        D = diag(*diagonal_entries)

        if P.det() == 0:
            raise ArithmeticError(
                "Eigenvector matrix is singular."
            )

        if not is_zero_matrix(A * P - P * D):
            raise ArithmeticError(
                "Diagonalization verification failed."
            )

        steps.append({
            "description": (
                "Assemble independent eigenvectors "
                "into P and eigenvalues into D."
            ),
            "latex": (
                rf"P={latex(P)},\quad D={latex(D)}"
            ),
        })

        steps.append({
            "description": (
                "Verify A = PDP^{-1}."
            ),
            "latex": (
                rf"A=PDP^{{-1}}={latex(A)}"
            ),
        })

    else:
        steps.append({
            "description": (
                "The number of independent eigenvectors "
                "is less than the matrix dimension. "
                "The matrix is not diagonalizable."
            ),
            "latex": (
                rf"\sum_\lambda "
                rf"\dim(E_\lambda)={len(all_vectors)}"
                rf"<{n}"
            ),
        })

    # Independent mathematical consistency checks.
    eigen_sum = sum(
        simplify(eigenvalue * algebraic_mult)
        for eigenvalue, algebraic_mult, _ in eigen_data
    )

    eigen_product = 1
    for eigenvalue, algebraic_mult, _ in eigen_data:
        eigen_product *= eigenvalue ** algebraic_mult

    verified = (
        simplify(eigen_sum - A.trace()) == 0
        and simplify(eigen_product - A.det()) == 0
        and all(item["verified"] for item in eigenvalues)
        and (
            not diagonalizable
            or is_zero_matrix(A * P - P * D)
        )
    )

    if not verified:
        raise ArithmeticError(
            "Eigenanalysis verification failed."
        )

    return {
        "input_latex": latex(A),
        "characteristic_polynomial": str(polynomial),
        "characteristic_latex": latex(polynomial),
        "factored_latex": latex(factored),
        "eigenvalues": eigenvalues,
        "diagonalizable": diagonalizable,
        "P_latex": latex(P) if P is not None else None,
        "D_latex": latex(D) if D is not None else None,
        "trace": str(A.trace()),
        "determinant": str(A.det()),
        "steps": steps,
        "verified": verified,
    }
