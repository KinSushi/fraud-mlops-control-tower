# Monitoring Plan

## Monitored dimensions

| Dimension | Metric |
|---|---|
| Data drift | PSI by feature |
| Prediction drift | predicted positive rate |
| Model quality | precision, recall, PR-AUC when labels exist |
| API reliability | latency, error rate, health endpoint |
| Governance | model card and data card freshness |

## Future implementation

- Evidently or NannyML report;
- Prometheus metrics endpoint;
- Grafana dashboard;
- scheduled scoring monitor;
- retraining trigger documentation.
