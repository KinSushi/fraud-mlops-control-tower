# Deployment Runbook

## Local API

```bash
make generate
make train
make api
```

Open:

```text
http://localhost:8000/docs
```

## Docker

```bash
make docker-build
make docker-run
```

## Rollback

For this local synthetic project, rollback means restoring the previous `artifacts/model.pkl` or retraining from generated data.

## Public-safety note

This is not a production deployment runbook.
