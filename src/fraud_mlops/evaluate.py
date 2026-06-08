"""Evaluate a persisted model against synthetic data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import average_precision_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score

from fraud_mlops.config import load_settings
from fraud_mlops.features import split_features_target


def evaluate_model(data_path: Path, model_path: Path, metrics_path: Path, threshold: float = 0.5) -> dict[str, object]:
    """Evaluate a persisted model and write metrics."""

    frame = pd.read_csv(data_path)
    features, target = split_features_target(frame)
    model = joblib.load(model_path)

    probabilities = model.predict_proba(features)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    matrix = confusion_matrix(target, predictions).tolist()

    metrics: dict[str, object] = {
        "precision": float(precision_score(target, predictions, zero_division=0)),
        "recall": float(recall_score(target, predictions, zero_division=0)),
        "f1": float(f1_score(target, predictions, zero_division=0)),
        "pr_auc": float(average_precision_score(target, probabilities)),
        "roc_auc": float(roc_auc_score(target, probabilities)),
        "threshold": float(threshold),
        "confusion_matrix": matrix,
    }

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    settings = load_settings()
    parser = argparse.ArgumentParser(description="Evaluate synthetic risk/anomaly model.")
    parser.add_argument("--data", default=str(settings.data_path))
    parser.add_argument("--model", default=str(settings.model_path))
    parser.add_argument("--metrics", default="reports/evaluation.json")
    parser.add_argument("--threshold", type=float, default=settings.threshold)
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""

    args = parse_args()
    metrics = evaluate_model(Path(args.data), Path(args.model), Path(args.metrics), args.threshold)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
