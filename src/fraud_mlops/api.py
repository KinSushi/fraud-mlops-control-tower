"""FastAPI serving layer for the synthetic risk/anomaly model."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from fraud_mlops.config import load_settings
from fraud_mlops.features import FEATURE_COLUMNS

app = FastAPI(
    title="fraud-mlops-control-tower",
    description="Synthetic risk/anomaly scoring API for public MLOps portfolio evidence.",
    version="0.1.0",
)


class RiskEventInput(BaseModel):
    """Prediction input schema."""

    amount_chf: float = Field(ge=0)
    hour: int = Field(ge=0, le=23)
    customer_tenure_days: int = Field(ge=0)
    channel_mobile: int = Field(ge=0, le=1)
    channel_web: int = Field(ge=0, le=1)
    channel_branch: int = Field(ge=0, le=1)
    channel_api: int = Field(ge=0, le=1)
    country_risk_score: float = Field(ge=0, le=1)
    previous_alerts_30d: int = Field(ge=0)
    velocity_1h: int = Field(ge=0)
    merchant_category_risk: float = Field(ge=0, le=1)
    source_system_risk: float = Field(ge=0, le=1)


class PredictionResponse(BaseModel):
    """Prediction response schema."""

    risk_score: float
    is_anomaly: bool
    threshold: float
    model_version: str


@lru_cache(maxsize=1)
def load_model() -> object:
    """Load the persisted model once."""

    settings = load_settings()
    model_path = Path(settings.model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {model_path}")
    return joblib.load(model_path)


@app.get("/health")
def health() -> dict[str, str]:
    """Health endpoint."""

    return {"status": "ok", "service": "fraud-mlops-control-tower"}


@app.get("/model-info")
def model_info() -> dict[str, object]:
    """Return model and feature metadata."""

    settings = load_settings()
    return {
        "model_path": str(settings.model_path),
        "threshold": settings.threshold,
        "features": FEATURE_COLUMNS,
        "data_policy": "synthetic-data-only",
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: RiskEventInput) -> PredictionResponse:
    """Score one synthetic risk/anomaly event."""

    settings = load_settings()
    try:
        model = load_model()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    row = [[getattr(payload, column) for column in FEATURE_COLUMNS]]
    risk_score = float(model.predict_proba(row)[0][1])
    return PredictionResponse(
        risk_score=risk_score,
        is_anomaly=risk_score >= settings.threshold,
        threshold=settings.threshold,
        model_version="local-artifact",
    )
