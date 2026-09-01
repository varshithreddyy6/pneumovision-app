"""Analyze a chest X-ray with DenseNet121 + Grad-CAM when a checkpoint is loaded."""

from __future__ import annotations

from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from starlette.concurrency import run_in_threadpool

from app import state
from app.config import DISCLAIMER
from app.schemas import AnalyzeResponse

router = APIRouter(prefix="/v1", tags=["analyze"])

ALLOWED = {"image/jpeg", "image/png", "image/jpg"}
MAX_BYTES = 15 * 1024 * 1024


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(..., description="Chest X-ray JPEG or PNG"),
) -> AnalyzeResponse:
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED and not (file.filename or "").lower().endswith(
        (".jpg", ".jpeg", ".png")
    ):
        raise HTTPException(
            status_code=415,
            detail={"code": "unsupported_type", "message": "Upload a JPEG or PNG.", "disclaimer": DISCLAIMER},
        )

    payload = await file.read()
    if not payload:
        raise HTTPException(
            status_code=400,
            detail={"code": "empty_file", "message": "The file was empty.", "disclaimer": DISCLAIMER},
        )
    if len(payload) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail={"code": "too_large", "message": "Max upload size is 15 MB.", "disclaimer": DISCLAIMER},
        )

    if state.engine is None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "model_not_loaded",
                "message": (
                    "No trained checkpoint. From services/api run: "
                    "python scripts/train_demo.py  then restart uvicorn."
                ),
                "disclaimer": DISCLAIMER,
            },
        )

    try:
        image = Image.open(BytesIO(payload))
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(
            status_code=400,
            detail={"code": "corrupt_image", "message": "Could not read that image.", "disclaimer": DISCLAIMER},
        ) from exc

    try:
        result = await run_in_threadpool(state.engine.predict, image)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail={
                "code": "inference_error",
                "message": f"{type(exc).__name__}: {exc}",
                "disclaimer": DISCLAIMER,
            },
        ) from exc
    return AnalyzeResponse(
        status="ok",
        label=result.label,
        probability_pneumonia=result.probability_pneumonia,
        probability_normal=result.probability_normal,
        threshold=result.threshold,
        uncertain=result.uncertain,
        review_recommended=result.review_recommended,
        confidence_band=result.confidence_band,
        message=(
            "Model score only — not a diagnosis. "
            + ("Human review recommended. " if result.review_recommended else "")
            + "Grad-CAM is attribution, not a lesion outline."
        ),
        filename=file.filename,
        heatmap_data_url=result.heatmap_data_url,
        overlay_data_url=result.overlay_data_url,
        untrained=result.untrained,
        disclaimer=DISCLAIMER,
    )
