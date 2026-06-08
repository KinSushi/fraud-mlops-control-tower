# Data Card — Synthetic Risk Events

## Dataset overview

| Field | Value |
|---|---|
| Dataset name | synthetic_risk_events.csv |
| Type | Synthetic |
| Sensitive data | None |
| Intended use | Public MLOps and model-governance demo |

## Columns

| Column | Description |
|---|---|
| event_id | Synthetic unique event identifier |
| amount_chf | Synthetic amount in CHF |
| hour | Event hour, 0-23 |
| customer_tenure_days | Synthetic tenure proxy |
| channel_mobile / web / branch / api | Binary channel flags |
| country_risk_score | Synthetic country-risk proxy |
| previous_alerts_30d | Synthetic previous-alert count |
| velocity_1h | Synthetic short-window event velocity |
| merchant_category_risk | Synthetic merchant-category proxy |
| source_system_risk | Synthetic source-system proxy |
| is_anomaly | Synthetic target label |

## Public-safety note

This dataset is generated and synthetic. It must not be interpreted as real banking, insurance, health, client or employer data.
