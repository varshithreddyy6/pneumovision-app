from fastapi import APIRouter

from app import state
from app.config import settings
from app.schemas import HealthResponse, ModelInfo

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    loaded = state.engine is not None
    note = (
        "DenseNet121 checkpoint loaded."
        if loaded
        else (
            "No checkpoint. Train one with: python scripts/train_demo.py "
            "(from services/api), then restart uvicorn."
        )
    )
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.api_version,
        model_loaded=loaded,
        note=note,
    )


@router.get("/v1/model", response_model=ModelInfo)
def model_info() -> ModelInfo:
    loaded = state.engine is not None
    return ModelInfo(
        loaded=loaded,
        note="densenet121" if loaded else "Checkpoint not loaded.",
    )
