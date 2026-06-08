# Risk Assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Synthetic data mismatch | Model may not reflect real distributions | State synthetic-only limitation |
| False positives | Operational workload | threshold policy and human review |
| False negatives | Missed anomaly | recall monitoring and periodic review |
| Drift | degraded performance | drift monitoring plan |
| Misuse | unsupported decisions | non-goals and public-safety notes |
| Privacy | accidental private data | synthetic-only rule and .gitignore |

## Human oversight

Any sensitive or real-world decision would require independent validation and human review. This repository does not support production decisioning.
