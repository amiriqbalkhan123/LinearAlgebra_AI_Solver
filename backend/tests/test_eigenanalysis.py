
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.engines.symbolic.eigenanalysis import (
    analyze_eigen,
)

client = TestClient(app)


def test_distinct_eigenvalues():
    result = analyze_eigen([
        ["4", "1"],
        ["0", "2"],
    ])

    values = {
        item["value"]
        for item in result["eigenvalues"]
    }

    assert values == {"2", "4"}
    assert result["diagonalizable"]
    assert result["verified"]


def test_repeated_diagonal_eigenvalue():
    result = analyze_eigen([
        ["3", "0"],
        ["0", "3"],
    ])

    assert len(result["eigenvalues"]) == 1

    item = result["eigenvalues"][0]

    assert item["algebraic_multiplicity"] == 2
    assert item["geometric_multiplicity"] == 2
    assert result["diagonalizable"]


def test_defective_matrix():
    result = analyze_eigen([
        ["2", "1"],
        ["0", "2"],
    ])

    item = result["eigenvalues"][0]

    assert item["algebraic_multiplicity"] == 2
    assert item["geometric_multiplicity"] == 1
    assert result["diagonalizable"] is False
    assert result["verified"]


def test_zero_matrix():
    result = analyze_eigen([
        ["0", "0"],
        ["0", "0"],
    ])

    assert result["diagonalizable"]
    assert result["determinant"] == "0"
    assert result["trace"] == "0"


def test_three_by_three():
    result = analyze_eigen([
        ["1", "0", "0"],
        ["0", "2", "0"],
        ["0", "0", "3"],
    ])

    assert len(result["eigenvalues"]) == 3
    assert result["diagonalizable"]
    assert result["verified"]


def test_fractional_matrix():
    result = analyze_eigen([
        ["1/2", "0"],
        ["0", "3/2"],
    ])

    values = {
        item["value"]
        for item in result["eigenvalues"]
    }

    assert values == {"1/2", "3/2"}
    assert result["verified"]


def test_complex_eigenvalues():
    result = analyze_eigen([
        ["0", "-1"],
        ["1", "0"],
    ])

    values = {
        item["value"]
        for item in result["eigenvalues"]
    }

    assert values == {"-I", "I"}
    assert result["diagonalizable"]
    assert result["verified"]


def test_single_element():
    result = analyze_eigen([["7"]])

    assert result["eigenvalues"][0]["value"] == "7"
    assert result["diagonalizable"]


def test_non_square_rejected():
    response = client.post(
        "/api/v1/eigenanalysis/analyze",
        json={
            "matrix": [
                ["1", "2", "3"],
                ["4", "5", "6"],
            ]
        },
    )

    assert response.status_code == 422


def test_size_limit():
    matrix = [
        ["1" if i == j else "0" for j in range(5)]
        for i in range(5)
    ]

    response = client.post(
        "/api/v1/eigenanalysis/analyze",
        json={"matrix": matrix},
    )

    assert response.status_code == 422


def test_api_success():
    response = client.post(
        "/api/v1/eigenanalysis/analyze",
        json={
            "matrix": [
                ["4", "1"],
                ["0", "2"],
            ]
        },
    )

    assert response.status_code == 200
    assert response.json()["verified"] is True
