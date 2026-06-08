from pathlib import Path

import pandas as pd

from fraud_mlops.features import FEATURE_COLUMNS, TARGET_COLUMN
from fraud_mlops.generate_synthetic_risk_data import RiskDataConfig, generate


def test_generate_synthetic_risk_data(tmp_path: Path) -> None:
    output = tmp_path / "synthetic_risk_events.csv"
    generate(RiskDataConfig(rows=200), output)

    frame = pd.read_csv(output)

    assert len(frame) == 200
    assert TARGET_COLUMN in frame.columns
    assert set(FEATURE_COLUMNS).issubset(frame.columns)
    assert set(frame[TARGET_COLUMN].unique()).issubset({0, 1})
    assert frame[TARGET_COLUMN].nunique() == 2
