
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

A = [["4", "1"], ["0", "2"]]
B = [["1", "2"], ["3", "4"]]


@pytest.mark.parametrize(
    "operation,expected",
    [
        ("determinant", "8"),
        ("rank", "2"),
        ("transpose", "Matrix([[4, 0], [1, 2]])"),
        ("rref", "Matrix([[1, 0], [0, 1]])"),
        ("inverse", "Matrix([[1/4, -1/8], [0, 1/2]])"),
    ],
)
def test_unary_operations(operation, expected):
    response = client.post(
        "/api/v1/solve/matrix",
        json={
            "matrix": A,
            "operation": operation,
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == expected


@pytest.mark.parametrize(
    "operation,expected",
    [
        ("addition", "Matrix([[5, 3], [3, 6]])"),
        ("subtraction", "Matrix([[3, -1], [-3, -2]])"),
        ("multiplication", "Matrix([[7, 12], [6, 8]])"),
    ],
)
def test_binary_operations(operation, expected):
    response = client.post(
        "/api/v1/solve/matrix",
        json={
            "matrix": A,
            "matrix_b": B,
            "operation": operation,
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == expected


def test_exact_fraction():
    response = client.post(
        "/api/v1/solve/matrix",
        json={
            "matrix": [["1/2"]],
            "operation": "inverse",
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == "Matrix([[2]])"


def test_invalid_dimensions():
    response = client.post(
        "/api/v1/solve/matrix",
        json={
            "matrix": [["1", "2"]],
            "matrix_b": [["3", "4"]],
            "operation": "multiplication",
        },
    )

    assert response.status_code == 400


def test_invalid_fraction():
    response = client.post(
        "/api/v1/solve/matrix",
        json={
            "matrix": [["1/0"]],
            "operation": "rank",
        },
    )

    assert response.status_code == 400


def test_invalid_row_lengths():
    response = client.post(
        "/api/v1/solve/matrix",
        json={
            "matrix": [["1", "2"], ["3"]],
            "operation": "rank",
        },
    )

    assert response.status_code == 422
