.PHONY: install generate train evaluate api mlflow-ui test lint ci docker-build docker-run clean

install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

generate:
	python -m fraud_mlops.generate_synthetic_risk_data --output data/synthetic_risk_events.csv --rows 2000

train:
	python -m fraud_mlops.train --data data/synthetic_risk_events.csv --model artifacts/model.pkl --metrics reports/metrics.json

evaluate:
	python -m fraud_mlops.evaluate --data data/synthetic_risk_events.csv --model artifacts/model.pkl --metrics reports/evaluation.json

api:
	uvicorn fraud_mlops.api:app --reload --host 127.0.0.1 --port 8000

mlflow-ui:
	mlflow ui --backend-store-uri mlruns --host 127.0.0.1 --port 5000

test:
	pytest

lint:
	ruff check .

ci: lint test

docker-build:
	docker build -t fraud-mlops-control-tower:local .

docker-run:
	docker run --rm -p 8000:8000 fraud-mlops-control-tower:local

clean:
	rm -f data/*.csv
	rm -f artifacts/*.pkl artifacts/*.json
	rm -f reports/*.json reports/*.csv
	rm -rf mlruns
