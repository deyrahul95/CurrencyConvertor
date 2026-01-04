from decimal import Decimal
from http import HTTPStatus


def test_convert_standard_success(client, mock_service_factory):
    # service returns a simple multiply by fixed rate
    def convert_fn(f, t, a):
        assert f == "USD"
        assert t == "EUR"
        return (a * Decimal("0.9")).quantize(Decimal("0.01"))

    mock_service_factory(convert_fn)

    resp = client.get(
        "/convert",
        params={"from_currency": "USD", "to_currency": "EUR", "amount": "100.00"},
    )
    assert resp.status_code == HTTPStatus.OK
    body = resp.json()
    assert (
        body["amount"] == "100.00"
        or body["amount"] == 100.00
        or body["amount"] == "100"
    )
    # The endpoint returns Decimal-serialised values; compare numeric values
    assert Decimal(str(body["result"])) == Decimal("90.00")
    assert Decimal(str(body["rate"])) == Decimal("0.90")
