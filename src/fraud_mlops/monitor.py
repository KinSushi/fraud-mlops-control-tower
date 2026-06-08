"""Monitoring report helpers for model outputs and synthetic data."""

from __future__ import annotations

import pandas as pd


def prediction_rate_summary(probabilities: pd.Series, threshold: float) -> dict[str, float]:
    """Return basic prediction-rate metrics."""

    predictions = probabilities >= threshold
    return {
        "rows": float(len(probabilities)),
        "avg_score": float(probabilities.mean()),
        "max_score": float(probabilities.max()),
        "predicted_positive_rate": float(predictions.mean()),
    }


def feature_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Return numeric feature summary."""

    return frame.describe().T.reset_index().rename(columns={"index": "feature"})
