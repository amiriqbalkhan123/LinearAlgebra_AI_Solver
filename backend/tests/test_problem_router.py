
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

URL = "/api/v1/problems/solve"


@pytest.mark.parametrize(
    "domain,payload",
    [
        (
            "matrices",
            {
                "operation": "determinant",
                "matrix": [["4", "1"], ["0", "2"]],
            },
        ),
        (
            "linear_systems",
            {
                "matrix": [["2", "1"], ["1", "-1"]],
                "constants": ["5", "1"],
            },
        ),
        (
            "vector_spaces",
            {
                "operation": "null_space",
                "matrix": [["1", "2"], ["2", "4"]],
            },
        ),
        (
            "vector_geometry",
            {
                "operation": "dot",
                "a": ["1", "2"],
                "b": ["3", "4"],
            },
        ),
        (
            "eigenanalysis",
            {
                "matrix": [["4", "1"], ["0", "2"]],
            },
        ),
        (
            "decompositions",
            {
                "operation": "pseudoinverse",
                "matrix": [["1", "0"], ["0", "2"]],
            },
        ),
    ],
)
def test_all_domains(domain, payload):
    response = client.post(
        URL,
        json={
            "domain": domain,
            "data": payload,
        },
    )

    assert response.status_code == 200, response.text

    body = response.json()

    assert body["domain"] == domain
    assert body["status"] == "success"
    assert body["verified"] is True
    assert isinstance(body["result"], dict)


def test_invalid_domain():
    response = client.post(
        URL,
        json={
            "domain": "calculus",
            "data": {},
        },
    )

    assert response.status_code == 422


def test_invalid_operation():
    response = client.post(
        URL,
        json={
            "domain": "matrices",
            "data": {
                "operation": "unknown",
                "matrix": [["1"]],
            },
        },
    )

    assert response.status_code == 422


def test_invalid_matrix():
    response = client.post(
        URL,
        json={
            "domain": "matrices",
            "data": {
                "operation": "determinant",
                "matrix": [["1", "2"], ["3"]],
            },
        },
    )

    assert response.status_code == 422


def test_mathematical_error():
    response = client.post(
        URL,
        json={
            "domain": "matrices",
            "data": {
                "operation": "inverse",
                "matrix": [["1", "2"], ["2", "4"]],
            },
        },
    )

    assert response.status_code == 400


def test_determinant_answer():
    response = client.post(
        URL,
        json={
            "domain": "matrices",
            "data": {
                "operation": "determinant",
                "matrix": [["4", "1"], ["0", "2"]],
            },
        },
    )
    

    assert response.status_code == 200
    assert response.json()["result"]["result"] == "8"
