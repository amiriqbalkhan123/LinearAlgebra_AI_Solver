
from io import BytesIO

from PIL import Image
from fastapi.testclient import TestClient

from app.main import app
from app.ai.ocr.image_processor import load_image

client = TestClient(app)
URL = "/api/v1/recognition/recognize"


def image_bytes(format="PNG"):
    image = Image.new("RGB", (200, 100), "white")
    output = BytesIO()
    image.save(output, format=format)
    return output.getvalue()


def test_image_loading():
    image = load_image(image_bytes())
    assert image.size == (200, 100)
    assert image.mode == "RGB"


def test_valid_text_recognition(monkeypatch):
    from app.api.v1 import recognition

    monkeypatch.setattr(
        recognition,
        "recognize_text",
        lambda image: "Find the determinant",
    )

    response = client.post(
        URL,
        data={"mode": "text"},
        files={
            "file": ("question.png", image_bytes(), "image/png")
        },
    )

    assert response.status_code == 200
    assert response.json()["recognized_text"] == (
        "Find the determinant"
    )
    assert response.json()["requires_confirmation"] is True


def test_valid_formula_recognition(monkeypatch):
    from app.api.v1 import recognition

    monkeypatch.setattr(
        recognition,
        "recognize_formula",
        lambda image: r"\det(A)=8",
    )

    response = client.post(
        URL,
        data={"mode": "formula"},
        files={
            "file": ("formula.png", image_bytes(), "image/png")
        },
    )

    assert response.status_code == 200
    assert response.json()["recognized_latex"] == r"\det(A)=8"


def test_invalid_file_type():
    response = client.post(
        URL,
        data={"mode": "text"},
        files={
            "file": ("test.txt", b"hello", "text/plain")
        },
    )
    assert response.status_code == 415


def test_corrupted_image():
    response = client.post(
        URL,
        data={"mode": "text"},
        files={
            "file": (
                "bad.png",
                b"not a real image",
                "image/png",
            )
        },
    )
    assert response.status_code == 400


def test_oversized_upload():
    response = client.post(
        URL,
        data={"mode": "text"},
        files={
            "file": (
                "large.png",
                b"x" * (5 * 1024 * 1024 + 1),
                "image/png",
            )
        },
    )
    assert response.status_code == 413


def test_invalid_mode():
    response = client.post(
        URL,
        data={"mode": "unknown"},
        files={
            "file": ("question.png", image_bytes(), "image/png")
        },
    )
    assert response.status_code == 422
