# Model Card — Synthetic Risk/Anomaly Classifier

## Model overview

| Field | Value |
|---|---|
| Model name | Synthetic risk/anomaly classifier |
| Status | Portfolio demo |
| Data type | Synthetic data only |
| Intended use | MLOps lifecycle demonstration |
| Out-of-scope use | Real decisioning, production operations, client impact |

## Intended use

Demonstrate feature engineering, model training, evaluation, serving, monitoring and governance documentation.

## Out-of-scope use

- No real client decisions.
- No production blocking or approval workflow.
- No financial, insurance or health decisioning.
- No real-world performance claims.

## Metrics

| Metric | Why it matters |
|---|---|
| Precision | Controls false positives |
| Recall | Controls missed anomalies |
| F1 | Balances precision and recall |
| PR-AUC | Better suited to imbalanced data |
| ROC-AUC | Ranking quality |
| Confusion matrix | Operational error analysis |

## Monitoring plan

- feature distribution drift;
- prediction-rate drift;
- precision/recall when labels are available;
- API latency and error rate;
- threshold review.

## Governance note

This model card is for public technical evidence. It is not a validated production model.
