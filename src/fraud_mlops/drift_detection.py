"""Simple drift-detection utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd


def population_stability_index(
    expected: pd.Series,
    actual: pd.Series,
    buckets: int = 10,
    epsilon: float = 1e-6,
) -> float:
    """Compute a simple Population Stability Index."""

    quantiles = np.linspace(0, 1, buckets + 1)
    breakpoints = np.unique(expected.quantile(quantiles).to_numpy())
    if len(breakpoints) < 3:
        return 0.0

    expected_counts, _ = np.histogram(expected, bins=breakpoints)
    actual_counts, _ = np.histogram(actual, bins=breakpoints)

    expected_pct = expected_counts / max(expected_counts.sum(), 1)
    actual_pct = actual_counts / max(actual_counts.sum(), 1)

    expected_pct = np.maximum(expected_pct, epsilon)
    actual_pct = np.maximum(actual_pct, epsilon)

    return float(np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)))
