
import pytest

from fastapi.testclient import TestClient
from app.main import app

from app.schemas.decomposition import DecompositionRequest
from app.engines.symbolic.decompositions import (
    analyze_decomposition,
)

client = TestClient(app)


def solve(operation, matrix, constants=None):
    request = DecompositionRequest(
        operation=operation,
        matrix=matrix,
        constants=constants,
    )
    return analyze_decomposition(request)


A = [["2", "1"], ["4", "3"]]


def test_lu():
    r = solve("lu", A)
    assert r["verified"]
    assert len(r["factors"]) == 3


def test_lu_row_swap():
    r = solve(
        "lu",
        [["0", "1"], ["2", "3"]],
    )
    assert r["verified"]


def test_qr():
    r = solve("qr", A)
    assert r["verified"]


def test_qr_rectangular():
    r = solve(
        "qr",
        [["1", "0"], ["0", "1"], ["1", "1"]],
    )
    assert r["verified"]


def test_svd():
    r = solve("svd", A)
    assert r["verified"]
    assert r["mode"] == "numerical"


def test_svd_rectangular():
    r = solve(
        "svd",
        [["1", "2", "3"], ["4", "5", "6"]],
    )
    assert r["verified"]


def test_pseudoinverse():
    r = solve("pseudoinverse", A)
    assert r["verified"]


def test_singular_pseudoinverse():
    r = solve(
        "pseudoinverse",
        [["1", "2"], ["2", "4"]],
    )
    assert r["verified"]


def test_least_squares():
    r = solve(
        "least_squares",
        [["1", "0"], ["0", "1"], ["1", "1"]],
        ["2", "3", "6"],
    )
    assert r["verified"]


def test_rank_deficient_least_squares():
    r = solve(
        "least_squares",
        [["1", "2"], ["2", "4"]],
        ["3", "6"],
    )
    assert r["verified"]


def test_spectral():
    r = solve(
        "spectral",
        [["2", "1"], ["1", "2"]],
    )
    assert r["verified"]


def test_repeated_spectral_eigenvalue():
    r = solve(
        "spectral",
        [["3", "0"], ["0", "3"]],
    )
    assert r["verified"]


def test_positive_definite():
    r = solve(
        "positive_definite",
        [["2", "1"], ["1", "2"]],
    )
    assert r["verified"]
    assert {
        m["name"]: m["value"]
        for m in r["metrics"]
    }["Positive definite"] == "True"


def test_not_positive_definite():
    r = solve(
        "positive_definite",
        [["1", "2"], ["2", "1"]],
    )
    assert r["verified"]
    assert {
        m["name"]: m["value"]
        for m in r["metrics"]
    }["Positive definite"] == "False"


def test_api():
    response = client.post(
        "/api/v1/decompositions/analyze",
        json={
            "operation": "lu",
            "matrix": A,
        },
    )
    assert response.status_code == 200
    assert response.json()["verified"]


def test_invalid_least_squares():
    response = client.post(
        "/api/v1/decompositions/analyze",
        json={
            "operation": "least_squares",
            "matrix": A,
            "constants": ["5"],
        },
    )
    assert response.status_code == 422


def test_non_square_spectral():
    response = client.post(
        "/api/v1/decompositions/analyze",
        json={
            "operation": "spectral",
            "matrix": [["1", "2", "3"]],
        },
    )
    assert response.status_code == 422


def test_non_symmetric_spectral():
    response = client.post(
        "/api/v1/decompositions/analyze",
        json={
            "operation": "spectral",
            "matrix": [["1", "2"], ["3", "4"]],
        },
    )
    assert response.status_code == 400
