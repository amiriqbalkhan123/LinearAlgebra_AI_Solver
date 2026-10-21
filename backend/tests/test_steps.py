
import pytest
from sympy import Matrix

from app.engines.step_by_step.elimination import (
    eliminate,
    inverse_with_steps,
    determinant_with_steps,
)


def test_ref():
    A = Matrix([
        [1, 2, 3],
        [2, 4, 7],
        [1, 1, 2],
    ])

    output = eliminate(A, reduced=False)

    assert output["matrix"].is_echelon
    assert output["matrix"].rank() == A.rank()
    assert len(output["steps"]) > 1


def test_rref():
    A = Matrix([
        [1, 2, 3],
        [2, 4, 7],
        [1, 1, 2],
    ])

    output = eliminate(A, reduced=True)

    assert output["matrix"] == A.rref()[0]
    assert output["matrix"] == Matrix.eye(3)


def test_row_swap():
    A = Matrix([
        [0, 2],
        [3, 4],
    ])

    output = eliminate(A)

    assert output["swaps"] == 1
    assert any(
        step["operation"] == "swap"
        for step in output["steps"]
    )


def test_inverse():
    A = Matrix([
        [4, 1],
        [0, 2],
    ])

    output = inverse_with_steps(A)

    assert output["matrix"] == A.inv()
    assert A * output["matrix"] == Matrix.eye(2)


def test_singular_inverse():
    A = Matrix([
        [1, 2],
        [2, 4],
    ])

    with pytest.raises(ValueError):
        inverse_with_steps(A)


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[4, 1], [0, 2]], 8),
        ([[0, 2], [3, 4]], -6),
        ([[1, 2], [2, 4]], 0),
        ([[5]], 5),
    ],
)
def test_determinants(data, expected):
    A = Matrix(data)

    output = determinant_with_steps(A)

    assert output["value"] == expected
    assert output["value"] == A.det()


def test_rectangular_rref():
    A = Matrix([
        [1, 2, 3],
        [2, 4, 6],
    ])

    output = eliminate(A, reduced=True)

    assert output["matrix"] == A.rref()[0]
