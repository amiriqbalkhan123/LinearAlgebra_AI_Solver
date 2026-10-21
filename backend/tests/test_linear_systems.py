
import pytest
from sympy import Matrix, symbols
from fastapi.testclient import TestClient

from app.main import app
from app.engines.symbolic.linear_systems import (
    solve_linear_system,
)

client = TestClient(app)


def test_unique_solution():
    result = solve_linear_system(
        [["2", "1"], ["1", "-1"]],
        ["5", "1"],
    )

    assert result["classification"] == "unique"
    assert result["solution"] == ["2", "1"]
    assert result["verified"]


def test_infinite_solutions():
    result = solve_linear_system(
        [["1", "2"], ["2", "4"]],
        ["5", "10"],
    )

    assert result["classification"] == "infinite"
    assert result["free_variables"] == ["x_2"]
    assert result["verified"]


def test_no_solution():
    result = solve_linear_system(
        [["1", "2"], ["2", "4"]],
        ["5", "11"],
    )

    assert result["classification"] == "no_solution"
    assert result["solution"] is None
    assert result["verified"]


def test_homogeneous_system():
    result = solve_linear_system(
        [["1", "2"], ["2", "4"]],
        ["0", "0"],
    )

    assert result["classification"] == "infinite"
    assert result["verified"]


def test_rectangular_system():
    result = solve_linear_system(
        [["1", "1", "1"], ["1", "-1", "0"]],
        ["3", "1"],
    )

    assert result["classification"] == "infinite"
    assert len(result["solution"]) == 3
    assert result["verified"]


def test_overdetermined_unique():
    result = solve_linear_system(
        [["1", "0"], ["0", "1"], ["1", "1"]],
        ["2", "3", "5"],
    )

    assert result["classification"] == "unique"
    assert result["solution"] == ["2", "3"]


def test_exact_fractions():
    result = solve_linear_system(
        [["2", "0"], ["0", "3"]],
        ["1", "1"],
    )

    assert result["solution"] == ["1/2", "1/3"]
    assert result["verified"]


def test_api_endpoint():
    response = client.post(
        "/api/v1/systems/solve",
        json={
            "matrix": [["2", "1"], ["1", "-1"]],
            "constants": ["5", "1"],
        },
    )

    assert response.status_code == 200
    assert response.json()["classification"] == "unique"


def test_invalid_dimensions():
    response = client.post(
        "/api/v1/systems/solve",
        json={
            "matrix": [["1", "2"], ["3", "4"]],
            "constants": ["5"],
        },
    )

    assert response.status_code == 422


def test_zero_denominator():
    response = client.post(
        "/api/v1/systems/solve",
        json={
            "matrix": [["1/0"]],
            "constants": ["1"],
        },
    )

    assert response.status_code == 400
