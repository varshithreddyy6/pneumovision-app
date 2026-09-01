from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf"
    b"\xc0\x00\x00\x00\x03\x00\x01\x00\x05\xfe\xd4&\x00\x00\x00\x00IEND\xaeB`\x82"
)


def test_health_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "model_loaded" in body


def test_metrics_are_not_fabricated() -> None:
    response = client.get("/v1/metrics")
    assert response.status_code == 200
    body = response.json()
    assert body["available"] is False
    assert body["metrics"] is None


def test_analyze_rejects_non_image() -> None:
    response = client.post(
        "/v1/analyze",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415


def test_analyze_png_contract() -> None:
    response = client.post(
        "/v1/analyze",
        files={"file": ("sample.png", PNG, "image/png")},
    )
    # No checkpoint → 503. With a checkpoint → 200 and a label.
    assert response.status_code in {200, 503}
    if response.status_code == 503:
        assert response.json()["detail"]["code"] == "model_not_loaded"
    else:
        body = response.json()
        assert body["status"] == "ok"
        assert body["label"] in {"NORMAL", "PNEUMONIA"}
        assert 0.0 <= body["probability_pneumonia"] <= 1.0
        assert body["heatmap_data_url"].startswith("data:image/png")
