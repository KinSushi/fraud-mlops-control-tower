import pandas as pd
import pytest

from fraud_mlops.features import FEATURE_COLUMNS, TARGET_COLUMN, split_features_target


def test_split_features_target() -> None:
    row = {column: 1 for column in FEATURE_COLUMNS}
    row[TARGET_COLUMN] = 0
    frame = pd.DataFrame([row])

    features, target = split_features_target(frame)

    assert list(features.columns) == FEATURE_COLUMNS
    assert target.tolist() == [0]


def test_split_features_target_rejects_missing_columns() -> None:
    with pytest.raises(ValueError, match="Missing required columns"):
        split_features_target(pd.DataFrame({"amount_chf": [1]}))
