"""Shared process state (the loaded model)."""

from __future__ import annotations

from typing import Optional

from app.ml.engine import InferenceEngine

engine: Optional[InferenceEngine] = None
