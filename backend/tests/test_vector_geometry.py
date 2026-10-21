
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.engines.symbolic.vector_geometry import (
    solve_vector_geometry,
)
from app.schemas.vector_geometry import (
    VectorGeometryRequest,
)

client = TestClient(app)


def solve(operation, **kwargs):
    return solve_vector_geometry(
        VectorGeometryRequest(
            operation=operation,
            **kwargs,
        )
    )


def test_addition():
    r = solve("addition", a=["1", "2"], b=["3", "4"])
    assert r["result"] == "Matrix([[4], [6]])"
    assert r["verified"]


def test_subtraction():
    r = solve("subtraction", a=["5", "7"], b=["2", "3"])
    assert r["result"] == "Matrix([[3], [4]])"


def test_scalar():
    r = solve("scalar", a=["2", "3"], scalar="1/2")
    assert r["result"] == "Matrix([[1], [3/2]])"


def test_dot():
    r = solve("dot", a=["1", "2", "3"], b=["4", "5", "6"])
    assert r["result"] == "32"


def test_cross():
    r = solve("cross", a=["1", "0", "0"], b=["0", "1", "0"])
    assert r["result"] == "Matrix([[0], [0], [1]])"


def test_outer():
    r = solve("outer", a=["1", "2"], b=["3", "4"])
    assert r["result"] == "Matrix([[3, 4], [6, 8]])"


def test_magnitude():
    r = solve("magnitude", a=["3", "4"])
    assert r["result"] == "5"


def test_normalize():
    r = solve("normalize", a=["3", "4"])
    assert r["verified"]
    assert r["result"] == "Matrix([[3/5], [4/5]])"


def test_distance():
    r = solve("distance", a=["1", "2"], b=["4", "6"])
    assert r["result"] == "5"


def test_orthogonality():
    r = solve("orthogonality", a=["1", "0"], b=["0", "2"])
    assert r["result"] is True


def test_projection():
    r = solve("projection", a=["3", "4"], b=["1", "0"])
    assert r["result"] == "Matrix([[3], [0]])"


def test_angle():
    r = solve("angle", a=["1", "0"], b=["0", "1"])
    assert r["result"] == "pi/2"
    assert r["verified"]


def test_span_member():
    r = solve(
        "span_membership",
        vectors=[["1", "0"], ["0", "1"]],
        target=["3", "4"],
    )
    assert r["result"] is True


def test_span_nonmember():
    r = solve(
        "span_membership",
        vectors=[["1", "0"], ["2", "0"]],
        target=["0", "1"],
    )
    assert r["result"] is False


def test_gram_schmidt():
    r = solve(
        "gram_schmidt",
        vectors=[["1", "0"], ["1", "1"]],
        normalize_basis=True,
    )
    assert r["verified"]
    assert len(r["result"]) == 2


def test_dependent_gram_schmidt():
    r = solve(
        "gram_schmidt",
        vectors=[["1", "2"], ["2", "4"]],
    )
    assert len(r["result"]) == 1
    assert r["verified"]


def test_zero_normalization_error():
    response = client.post(
        "/api/v1/vector-geometry/solve",
        json={"operation": "normalize", "a": ["0", "0"]},
    )
    assert response.status_code == 400


def test_dimension_error():
    response = client.post(
        "/api/v1/vector-geometry/solve",
        json={
            "operation": "addition",
            "a": ["1", "2"],
            "b": ["1", "2", "3"],
        },
    )
    assert response.status_code == 422


def test_invalid_cross_dimension():
    response = client.post(
        "/api/v1/vector-geometry/solve",
        json={
            "operation": "cross",
            "a": ["1", "2"],
            "b": ["3", "4"],
        },
    )
    assert response.status_code == 422


def test_api():
    response = client.post(
        "/api/v1/vector-geometry/solve",
        json={
            "operation": "dot",
            "a": ["1", "2"],
            "b": ["3", "4"],
        },
    )
    assert response.status_code == 200
    assert response.json()["result"] == "11"
