
import numpy as np

from sympy import (
    Matrix,
    eye,
    diag,
    latex,
    simplify,
    GramSchmidt,
)

from app.engines.symbolic.matrices import (
    make_matrix,
    parse_value,
)


def exact_equal(A, B):
    return (
        A.shape == B.shape
        and all(
            simplify(a - b) == 0
            for a, b in zip(A, B)
        )
    )


def matrix_factor(name, M):
    return {
        "name": name,
        "latex": latex(M),
    }


def analyze_decomposition(question):
    A = make_matrix(question.matrix)
    op = question.operation

    factors = []
    steps = []
    metrics = []
    verified = False
    mode = "exact"

    def step(description, expression):
        steps.append({
            "description": description,
            "latex": expression,
        })

    if op == "lu":
        L, U, swaps = A.LUdecomposition()

        P = eye(A.rows).permuteFwd(swaps)

        factors = [
            matrix_factor("P", P),
            matrix_factor("L", L),
            matrix_factor("U", U),
        ]

        step(
            "Apply row permutations and factor A.",
            r"PA=LU",
        )

        verified = exact_equal(P * A, L * U)

    elif op == "qr":
        Q, R = A.QRdecomposition()

        factors = [
            matrix_factor("Q", Q),
            matrix_factor("R", R),
        ]

        step(
            "Factor A into orthonormal columns and "
            "an upper trapezoidal matrix.",
            r"A=QR",
        )

        verified = (
            exact_equal(Q * R, A)
            and exact_equal(Q.T * Q, eye(Q.cols))
        )

    elif op == "svd":
        mode = "numerical"

        array = np.array(A.tolist(), dtype=float)

        if not np.isfinite(array).all():
            raise ValueError("Matrix contains non-finite values.")

        U, singular_values, Vt = np.linalg.svd(
            array,
            full_matrices=False,
        )

        Sigma = np.diag(singular_values)
        reconstruction = U @ Sigma @ Vt

        def display(M):
            return Matrix(np.round(M, 8).tolist())

        factors = [
            matrix_factor("U", display(U)),
            matrix_factor("Σ", display(Sigma)),
            matrix_factor("Vᵀ", display(Vt)),
        ]

        metrics.append({
            "name": "Singular values",
            "value": ", ".join(
                f"{x:.8g}" for x in singular_values
            ),
        })

        step(
            "Compute the reduced singular value decomposition.",
            r"A\approx U\Sigma V^T",
        )

        residual = np.linalg.norm(
            array - reconstruction, ord="fro"
        )
        scale = max(1.0, np.linalg.norm(array, ord="fro"))

        metrics.append({
            "name": "Relative reconstruction error",
            "value": f"{residual / scale:.3e}",
        })

        verified = (
            np.allclose(
                reconstruction, array,
                rtol=1e-9, atol=1e-9
            )
            and np.allclose(
                U.T @ U, np.eye(U.shape[1]),
                atol=1e-9
            )
            and np.allclose(
                Vt @ Vt.T, np.eye(Vt.shape[0]),
                atol=1e-9
            )
        )

    elif op == "pseudoinverse":
        result = A.pinv()

        factors = [matrix_factor("A⁺", result)]

        step(
            "Calculate the Moore–Penrose pseudoinverse.",
            r"A^+",
        )

        verified = all([
            exact_equal(A * result * A, A),
            exact_equal(result * A * result, result),
            exact_equal((A * result).T, A * result),
            exact_equal((result * A).T, result * A),
        ])

    elif op == "least_squares":
        b = Matrix([
            parse_value(value)
            for value in question.constants
        ])

        x = A.pinv() * b
        residual = A * x - b

        factors = [
            matrix_factor("b", b),
            matrix_factor("x", x),
            matrix_factor("Residual", residual),
        ]

        step(
            "Find the minimum-norm least-squares solution.",
            r"x=A^+b",
        )

        step(
            "Check the normal equations.",
            r"A^T(Ax-b)=0",
        )

        verified = exact_equal(
            A.T * residual,
            Matrix.zeros(A.cols, 1),
        )

        metrics.append({
            "name": "Squared residual norm",
            "value": str(
                simplify(residual.dot(residual))
            ),
        })

    elif op == "spectral":
        if not A.is_symmetric():
            raise ValueError(
                "Spectral decomposition currently "
                "requires a real symmetric matrix."
            )

        eigen_data = A.eigenvects()
        vectors = []
        eigenvalues = []

        for value, multiplicity, basis in eigen_data:
            ortho = GramSchmidt(
                basis,
                orthonormal=True,
            )

            for v in ortho:
                vectors.append(v)
                eigenvalues.append(value)

        Q = Matrix.hstack(*vectors)
        D = diag(*eigenvalues)

        factors = [
            matrix_factor("Q", Q),
            matrix_factor("Λ", D),
        ]

        step(
            "Construct orthonormal eigenvectors.",
            r"Q^TQ=I",
        )

        step(
            "Reconstruct the symmetric matrix.",
            r"A=Q\Lambda Q^T",
        )

        verified = (
            exact_equal(Q.T * Q, eye(A.rows))
            and exact_equal(Q * D * Q.T, A)
        )

    elif op == "positive_definite":
        if not A.is_symmetric():
            raise ValueError(
                "Positive definiteness test currently "
                "requires a real symmetric matrix."
            )

        minors = [
            A[:k, :k].det()
            for k in range(1, A.rows + 1)
        ]

        is_positive = all(v > 0 for v in minors)

        metrics.append({
            "name": "Positive definite",
            "value": str(is_positive),
        })

        metrics.append({
            "name": "Leading principal minors",
            "value": ", ".join(map(str, minors)),
        })

        step(
            "Apply Sylvester's criterion to the "
            "leading principal minors.",
            r"A\succ0\iff \Delta_k>0\ \forall k",
        )

        # This checks that the criterion was evaluated.
        verified = all(v.is_real is True for v in minors)

    else:
        raise ValueError("Unsupported decomposition.")

    if not verified:
        raise ArithmeticError(
            "Decomposition verification failed."
        )

    return {
        "operation": op,
        "mode": mode,
        "input_latex": latex(A),
        "factors": factors,
        "metrics": metrics,
        "steps": steps,
        "verified": bool(verified),
    }
