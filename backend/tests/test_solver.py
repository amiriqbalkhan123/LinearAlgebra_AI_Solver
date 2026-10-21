
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_determinant():
    response = client.post(
        "/api/v1/solve/matrix",
        json={
            "matrix": [[4, 1], [0, 2]],
            "operation": "determinant",
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == "8"


def test_invalid_matrix():
    response = client.post(
        "/api/v1/solve/matrix",
        json={
            "matrix": [[1, 2], [3]],
            "operation": "rank",
        },
    )

    assert response.status_code == 422
