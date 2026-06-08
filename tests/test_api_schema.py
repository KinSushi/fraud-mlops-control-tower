from fastapi.testclient import TestClient

from fraud_mlops.api import RiskEventInput, app


def test_risk_event_input_schema() -> None:
    event = RiskEventInput(
        amount_chf=100.0,
        hour=12,
        customer_tenure_days=300,
        channel_mobile=1,
        channel_web=0,
        channel_branch=0,
        channel_api=0,
        country_risk_score=0.2,
        previous_alerts_30d=0,
        velocity_1h=2,
        merchant_category_risk=0.1,
        source_system_risk=0.1,
    )

    assert event.amount_chf == 100.0


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
