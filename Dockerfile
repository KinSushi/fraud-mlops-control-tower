FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY artifacts ./artifacts

RUN python -m pip install --upgrade pip && pip install .

EXPOSE 8000

CMD ["uvicorn", "fraud_mlops.api:app", "--host", "0.0.0.0", "--port", "8000"]
