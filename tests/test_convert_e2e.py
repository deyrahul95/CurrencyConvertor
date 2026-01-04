from decimal import Decimal
from http import HTTPStatus
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_convert_e2e_success():
    resp = client.get(
        "/convert",
        params={"from_currency": "USD", "to_currency": "INR", "amount": 100},
    )
    assert resp.status_code == HTTPStatus.OK
    body = resp.json()

    # Basic sanity checks: amounts present and numeric
    assert "amount" in body and "result" in body
    assert Decimal(str(body["amount"])) == Decimal(100)
    assert Decimal(str(body["result"])) > Decimal(0)
    assert Decimal(str(body["rate"])) > Decimal(0)


def test_convert_post_e2e_success():
    resp = client.post(
        "/convert",
        json={"from_currency": "USD", "to_currency": "INR", "amount": 100},
    )
    assert resp.status_code == HTTPStatus.OK
    body = resp.json()

    # Basic sanity checks: amounts present and numeric
    assert "amount" in body and "result" in body
    assert Decimal(str(body["amount"])) == Decimal(100)
    assert Decimal(str(body["result"])) > Decimal(0)
    assert Decimal(str(body["rate"])) > Decimal(0)


def test_convert_e2e_failed():
    resp = client.get(
        "/convert",
        params={"from_currency": "ABC", "to_currency": "CDE", "amount": 100},
    )
    assert resp.status_code == HTTPStatus.NOT_FOUND

    body = resp.json()

    assert "detail" in body
    assert body["detail"] == "Exchange rate from ABC to CDE is not available."


def test_convert_post_e2e_failed():
    resp = client.post(
        "/convert",
        json={"from_currency": "ABC", "to_currency": "CDE", "amount": "100"},
    )
    assert resp.status_code == HTTPStatus.NOT_FOUND

    body = resp.json()

    assert "detail" in body
    assert body["detail"] == "Conversation rate not found form ABC to CDE currency."
