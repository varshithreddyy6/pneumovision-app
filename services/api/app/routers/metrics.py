from fastapi import APIRouter

from app.schemas import MetricsResponse

router = APIRouter(prefix="/v1", tags=["metrics"])


@router.get("/metrics", response_model=MetricsResponse)
def metrics() -> MetricsResponse:
    """Honest empty state. Do not invent an AUROC in this foundation."""
    return MetricsResponse()
