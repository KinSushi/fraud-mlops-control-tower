"""Model training with MLflow logging."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from fraud_mlops.config import load_settings
from fraud_mlops.features import split_features_target


def select_threshold_for_f1(y_true: pd.Series, probabilities: object) -> float:
    """Select a decision threshold that maximizes F1 on validation data.

    The project is synthetic and public. This function demonstrates threshold-selection
    mechanics for imbalanced risk/anomaly data; it is not a production risk policy.
    """

    precision, recall, thresholds = precision_recall_curve(y_true, probabilities)
    if len(thresholds) == 0:
        return 0.5

    best_threshold = float(thresholds[0])
    best_f1 = -1.0
    for candidate, candidate_precision, candidate_recall in zip(
        thresholds,
        precision[:-1],
        recall[:-1],
        strict=False,
    ):
        denominator = candidate_precision + candidate_recall
        candidate_f1 = 0.0 if denominator == 0 else 2 * candidate_precision * candidate_recall / denominator
        if candidate_f1 > best_f1:
            best_f1 = float(candidate_f1)
            best_threshold = float(candidate)

    return best_threshold


def train_model(
    data_path: Path,
    model_path: Path,
    metrics_path: Path,
    threshold: float | None = None,
) -> dict[str, float]:
    """Train a baseline model and persist model + metrics."""

    frame = pd.read_csv(data_path)
    features, target = split_features_target(frame)

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.25,
        random_state=42,
        stratify=target,
    )

    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )

    settings = load_settings()
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment("fraud-mlops-control-tower")

    with mlflow.start_run(run_name="random_forest_baseline"):
        model.fit(x_train, y_train)
        probabilities = model.predict_proba(x_test)[:, 1]
        selected_threshold = threshold if threshold is not None else select_threshold_for_f1(y_test, probabilities)
        predictions = (probabilities >= selected_threshold).astype(int)

        metrics = {
            "precision": float(precision_score(y_test, predictions, zero_division=0)),
            "recall": float(recall_score(y_test, predictions, zero_division=0)),
            "f1": float(f1_score(y_test, predictions, zero_division=0)),
            "pr_auc": float(average_precision_score(y_test, probabilities)),
            "roc_auc": float(roc_auc_score(y_test, probabilities)),
            "threshold": float(selected_threshold),
            "positive_rate": float(target.mean()),
        }

        mlflow.log_params(
            {
                "model_type": "RandomForestClassifier",
                "n_estimators": 120,
                "max_depth": 8,
                "class_weight": "balanced",
                "threshold_policy": "max_f1_on_validation" if threshold is None else "manual_threshold",
            }
        )
        mlflow.log_metrics(metrics)

        model_path.parent.mkdir(parents=True, exist_ok=True)
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, model_path)
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        mlflow.log_artifact(str(metrics_path))
        mlflow.sklearn.log_model(model, artifact_path="model")

    return metrics


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    settings = load_settings()
    parser = argparse.ArgumentParser(description="Train synthetic risk/anomaly model.")
    parser.add_argument("--data", default=str(settings.data_path))
    parser.add_argument("--model", default=str(settings.model_path))
    parser.add_argument("--metrics", default=str(settings.metrics_path))
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Optional manual threshold. Defaults to validation F1 threshold tuning.",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""

    args = parse_args()
    metrics = train_model(Path(args.data), Path(args.model), Path(args.metrics), args.threshold)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
