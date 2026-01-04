import pytest
from decimal import Decimal
from pydantic import ValidationError
from models.convert_response import ConvertResponse


def test_valid_conversion():
    response = ConvertResponse(amount=Decimal("100"), result=Decimal("91"))
    assert response.amount == Decimal("100")
    assert response.result == Decimal("91")
    assert response.rate == Decimal("0.91")


def test_zero_amount():
    with pytest.raises(ValidationError) as excinfo:
        ConvertResponse(amount=Decimal("0"), result=Decimal("150"))
    assert "Input should be greater than 0" in str(excinfo.value)


def test_negative_amount():
    with pytest.raises(ValidationError) as excinfo:
        ConvertResponse(amount=Decimal("-50"), result=Decimal("150"))
    assert "Input should be greater than 0" in str(excinfo.value)


def test_zero_result():
    with pytest.raises(ValidationError) as excinfo:
        ConvertResponse(amount=Decimal("100"), result=Decimal("0"))
    assert "Input should be greater than 0" in str(excinfo.value)


def test_negative_result():
    with pytest.raises(ValidationError) as excinfo:
        ConvertResponse(amount=Decimal("100"), result=Decimal("-2.6"))
    assert "Input should be greater than 0" in str(excinfo.value)


def test_large_numbers():
    response = ConvertResponse(amount=Decimal("1000000"), result=Decimal("910000"))
    assert response.rate == Decimal("0.91")


def test_edge_case():
    response = ConvertResponse(amount=Decimal("1"), result=Decimal("1"))
    assert response.rate == Decimal("1.00")


def test_default_rate():
    response = ConvertResponse(amount=Decimal("100"), result=Decimal("100"))
    assert response.rate == Decimal("1.00")


def test_calculate_rate_when_zero_amount():
    response = ConvertResponse(amount=Decimal("1"), result=Decimal("1"))
    assert response.rate == Decimal("1.00")
