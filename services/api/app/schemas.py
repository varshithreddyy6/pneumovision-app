from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    model_loaded: bool = False
    note: str


class AnalyzeResponse(BaseModel):
    status: str
    label: Optional[str] = None
    probability_pneumonia: Optional[float] = None
    probability_normal: Optional[float] = None
    threshold: float = 0.5
    uncertain: bool = True
    review_recommended: bool = True
    confidence_band: Optional[str] = None
    message: str
    filename: Optional[str] = None
    heatmap_data_url: Optional[str] = None
    overlay_data_url: Optional[str] = None
    untrained: bool = False
    disclaimer: str


class MetricsResponse(BaseModel):
    available: bool = False
    message: str = "Metrics are never fabricated. Train and evaluate to populate this resource."
    metrics: Optional[dict] = None


class ModelInfo(BaseModel):
    name: str = "densenet121"
    loaded: bool = False
    note: str = ""


class ErrorBody(BaseModel):
    code: str
    message: str
    disclaimer: str
