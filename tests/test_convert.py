import pytest
from fastapi.testclient import TestClient
from main import (
    app,
    RATES,
)

client = TestClient(app)


# Test data
@pytest.mark.parametrize(
    "from_currency, to_currency, amount, expected_rate",
    [
        ("USD", "EUR", 10, 0.9),  
        ("EUR", "USD", 5, 1.1),
        ("usd", "eur", 2.5, 0.9),
    ],
)
def test_convert_endpoint(from_currency, to_currency, amount, expected_rate):
    # Ensure the RATES dict has the expected keys for the test
    key = (from_currency.upper(), to_currency.upper())
    RATES[key] = expected_rate

    response = client.get(
        "/convert",
        params={
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == amount
    assert data["rate"] == expected_rate
    assert data["result"] == pytest.approx(amount * expected_rate)
