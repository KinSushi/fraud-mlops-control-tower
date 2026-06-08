import pandas as pd

from fraud_mlops.monitor import prediction_rate_summary


def test_prediction_rate_summary() -> None:
    summary = prediction_rate_summary(pd.Series([0.1, 0.6, 0.8]), threshold=0.5)

    assert summary["rows"] == 3.0
    assert summary["predicted_positive_rate"] == 2 / 3
