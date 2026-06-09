# Validation

## Purpose

This file documents the local and CI validation path for this repository.

## Static validation

```powershell
python -m compileall -q src tests
python -m pytest -q --maxfail=1
python -m ruff check .
```

## MLOps execution checks

```powershell
python -m fraud_mlops.generate_synthetic_risk_data --output data/synthetic_risk_events.csv --rows 100
python -m fraud_mlops.train --data data/synthetic_risk_events.csv --model artifacts/model.pkl --metrics reports/metrics.json
python -m fraud_mlops.evaluate --data data/synthetic_risk_events.csv --model artifacts/model.pkl --metrics reports/evaluation.json
```

Optional local services:

```powershell
python -m uvicorn fraud_mlops.api:app --host 127.0.0.1 --port 8000
python -m mlflow ui --backend-store-uri mlruns --host 127.0.0.1 --port 5000
```

## Public-safety validation

```powershell
Get-ChildItem -Recurse -File |
  Where-Object { $_.FullName -notmatch "\\.git\\" -and $_.FullName -notmatch "\\.venv\\" } |
  Select-String -Pattern "BEGIN .*PRIVATE KEY","gho_","api_key","secret","token","password"
```

Expected review notes:

- `.env.example` may contain local placeholder names.
- `.gitignore` and documentation may contain safety words such as `secret` or `password`.
- Real credentials must never appear.

## Portfolio rule

This repository is public technical evidence. It must not contain CVs, cover letters, salary targets, private school documents, real client data, employer data, credentials or production decisioning claims.
