
import pytest
from fastapi.testclient import TestClient
from sympy import Matrix

from app.main import app
from app.engines.symbolic.vector_spaces import (
    solve_vector_space,
)

client = TestClient(app)

A = [
    ["1", "2", "3"],
    ["2", "4", "6"],
]


def test_column_space():
    result = solve_vector_space(A, "column_space")

    assert result["dimension"] == 1
    assert result["pivot_columns"] == [1]
    assert result["basis"] == [["1", "2"]]
    assert result["verified"]


def test_row_space():
    result = solve_vector_space(A, "row_space")

    assert result["dimension"] == 1
    assert result["verified"]


def test_null_space():
    result = solve_vector_space(A, "null_space")

    assert result["dimension"] == 2
    assert result["nullity"] == 2
    assert len(result["basis"]) == 2
    assert result["verified"]


def test_left_null_space():
    result = solve_vector_space(A, "left_null_space")

    assert result["dimension"] == 1
    assert result["verified"]


def test_rank_nullity():
    result = solve_vector_space(A, "rank_nullity")

    assert result["rank"] == 1
    assert result["nullity"] == 2
    assert result["verified"]


def test_dependent_columns():
    result = solve_vector_space(A, "independence")

    assert result["is_independent"] is False


def test_independent_columns():
    result = solve_vector_space(
        [["1", "0"], ["0", "1"]],
        "independence",
    )

    assert result["is_independent"] is True


def test_zero_matrix():
    result = solve_vector_space(
        [["0", "0"], ["0", "0"]],
        "null_space",
    )

    assert result["rank"] == 0
    assert result["nullity"] == 2
    assert result["verified"]


def test_api():
    response = client.post(
        "/api/v1/vector-spaces/solve",
        json={
            "matrix": A,
            "operation": "null_space",
        },
    )

    assert response.status_code == 200
    assert response.json()["verified"] is True


def test_invalid_matrix():
    response = client.post(
        "/api/v1/vector-spaces/solve",
        json={
            "matrix": [["1", "2"], ["3"]],
            "operation": "null_space",
        },
    )

    assert response.status_code == 422
