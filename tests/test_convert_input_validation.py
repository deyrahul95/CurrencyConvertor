from http import HTTPStatus


def test_invalid_currency_length_short(client):
    resp = client.get(
        "/convert",
        params={"from_currency": "US", "to_currency": "EUR", "amount": "1.00"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_currency_length_short_post(client):
    resp = client.post(
        "/convert",
        json={"from_currency": "US", "to_currency": "EUR", "amount": "1.00"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_currency_length_long(client):
    resp = client.get(
        "/convert",
        params={"from_currency": "USDA", "to_currency": "EUR", "amount": "1.00"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_currency_length_long_post(client):
    resp = client.post(
        "/convert",
        json={"from_currency": "USDA", "to_currency": "EUR", "amount": "1.00"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_amount_not_decimal(client):
    resp = client.get(
        "/convert",
        params={"from_currency": "USD", "to_currency": "EUR", "amount": "abc"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_amount_not_decimal_post(client):
    resp = client.post(
        "/convert",
        json={"from_currency": "USD", "to_currency": "EUR", "amount": "abc"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_amount_negative(client):
    resp = client.get(
        "/convert",
        params={"from_currency": "USD", "to_currency": "EUR", "amount": "-5.00"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_amount_negative_post(client):
    resp = client.post(
        "/convert",
        json={"from_currency": "USD", "to_currency": "EUR", "amount": "-5.00"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_amount_zero(client):
    resp = client.get(
        "/convert",
        params={"from_currency": "USD", "to_currency": "EUR", "amount": "0.00"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_amount_zero_post(client):
    resp = client.post(
        "/convert",
        json={"from_currency": "USD", "to_currency": "EUR", "amount": "0.00"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_amount_too_many_decimal_places(client):
    # amount requires decimal_places=2 per Query(...)
    resp = client.get(
        "/convert",
        params={"from_currency": "USD", "to_currency": "EUR", "amount": "1.234"},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
