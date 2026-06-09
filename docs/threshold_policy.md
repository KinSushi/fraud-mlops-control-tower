# Threshold Policy

## Purpose

This repository demonstrates threshold mechanics for synthetic risk/anomaly analytics. It does not define a production risk policy.

---

## Training-time threshold

By default, `src/fraud_mlops/train.py` selects a validation threshold that maximizes F1 on the held-out validation split.

This is useful for the public portfolio because it proves that the model lifecycle does not rely blindly on the arbitrary `0.50` threshold.

```text
selected threshold = argmax(F1) on validation probabilities
```

The generated metrics report includes:

- precision;
- recall;
- F1;
- PR-AUC;
- ROC-AUC;
- selected threshold;
- positive rate.

---

## Manual threshold override

A manual threshold can still be supplied:

```bash
python -m fraud_mlops.train \
  --data data/synthetic_risk_events.csv \
  --model artifacts/model.pkl \
  --metrics reports/metrics.json \
  --threshold 0.50
```

When no manual threshold is supplied, validation F1 tuning is used.

---

## Why threshold matters

In anomaly and risk workflows, threshold selection controls the trade-off between:

- false positives, which create operational workload;
- false negatives, which miss relevant anomalies.

Accuracy is not the main metric for imbalanced risk/anomaly data.

---

## Public portfolio boundary

This policy is a technical demonstration only.

It is not:

- a production fraud policy;
- a credit, insurance, health or financial decision policy;
- a validated model-risk framework;
- an automated decisioning rule.

---

## Future improvements

- precision/recall curve visualization;
- cost-sensitive threshold selection;
- recall-constrained thresholding;
- class-specific review workflow;
- human-in-the-loop escalation;
- model-risk approval checklist.
