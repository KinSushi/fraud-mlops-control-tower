"""Runtime settings for fraud-mlops-control-tower."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Local project settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    data_path: Path = Field(
        default=Path("data/synthetic_risk_events.csv"),
        validation_alias="FRAUD_MLOPS_DATA_PATH",
    )
    model_path: Path = Field(
        default=Path("artifacts/model.pkl"),
        validation_alias="FRAUD_MLOPS_MODEL_PATH",
    )
    metrics_path: Path = Field(
        default=Path("reports/metrics.json"),
        validation_alias="FRAUD_MLOPS_METRICS_PATH",
    )
    threshold: float = Field(default=0.50, validation_alias="FRAUD_MLOPS_THRESHOLD")
    mlflow_tracking_uri: str = Field(default="mlruns", validation_alias="MLFLOW_TRACKING_URI")


def load_settings() -> Settings:
    """Load settings."""

    return Settings()
