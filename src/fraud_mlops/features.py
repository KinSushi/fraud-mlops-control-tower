"""Feature engineering helpers for synthetic risk/anomaly modeling."""

from __future__ import annotations

import pandas as pd

FEATURE_COLUMNS = [
    "amount_chf",
    "hour",
    "customer_tenure_days",
    "channel_mobile",
    "channel_web",
    "channel_branch",
    "channel_api",
    "country_risk_score",
    "previous_alerts_30d",
    "velocity_1h",
    "merchant_category_risk",
    "source_system_risk",
]
TARGET_COLUMN = "is_anomaly"


def validate_columns(frame: pd.DataFrame) -> None:
    """Validate that all required columns exist."""

    required = [*FEATURE_COLUMNS, TARGET_COLUMN]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def split_features_target(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return X/y after validating required columns."""

    validate_columns(frame)
    return frame[FEATURE_COLUMNS].copy(), frame[TARGET_COLUMN].astype(int).copy()
