"""Synthetic risk/anomaly dataset generator."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
import random


@dataclass(frozen=True)
class RiskDataConfig:
    """Synthetic risk dataset configuration."""

    rows: int = 2000
    seed: int = 42


FIELDS = [
    "event_id",
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
    "is_anomaly",
]


def generate(config: RiskDataConfig, output_path: Path) -> None:
    """Generate a deterministic synthetic risk/anomaly dataset."""

    rng = random.Random(config.seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()

        for index in range(config.rows):
            amount = round(rng.lognormvariate(4.2, 0.9), 2)
            if index % 173 == 0:
                amount = round(rng.uniform(8000, 75000), 2)

            hour = rng.randint(0, 23)
            tenure = rng.randint(1, 4000)
            previous_alerts = rng.choices([0, 1, 2, 3, 4], weights=[78, 13, 6, 2, 1])[0]
            velocity = rng.randint(1, 30)
            country_risk = round(rng.random(), 3)
            merchant_risk = round(rng.random(), 3)
            source_system_risk = round(rng.random(), 3)
            channel = rng.choice(["mobile", "web", "branch", "api"])

            score = (
                (amount > 8000) * 0.22
                + (hour < 5) * 0.12
                + (tenure < 90) * 0.14
                + (previous_alerts >= 2) * 0.24
                + (velocity > 12) * 0.14
                + (country_risk > 0.8) * 0.14
                + (merchant_risk > 0.85) * 0.12
                + (source_system_risk > 0.85) * 0.10
                + rng.random() * 0.10
            )
            is_anomaly = int(score > 0.45)

            writer.writerow(
                {
                    "event_id": f"EVT-{index + 1:08d}",
                    "amount_chf": amount,
                    "hour": hour,
                    "customer_tenure_days": tenure,
                    "channel_mobile": int(channel == "mobile"),
                    "channel_web": int(channel == "web"),
                    "channel_branch": int(channel == "branch"),
                    "channel_api": int(channel == "api"),
                    "country_risk_score": country_risk,
                    "previous_alerts_30d": previous_alerts,
                    "velocity_1h": velocity,
                    "merchant_category_risk": merchant_risk,
                    "source_system_risk": source_system_risk,
                    "is_anomaly": is_anomaly,
                }
            )


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description="Generate synthetic risk/anomaly data.")
    parser.add_argument("--output", default="data/synthetic_risk_events.csv")
    parser.add_argument("--rows", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""

    args = parse_args()
    generate(RiskDataConfig(rows=args.rows, seed=args.seed), Path(args.output))
    print(f"Generated {args.rows} synthetic risk events at {args.output}")


if __name__ == "__main__":
    main()
