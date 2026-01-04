from decimal import Decimal
from fastapi import APIRouter, Depends, Query


from convert_response import ConvertResponse
from exchange_service import ExchangeService

router = APIRouter()


@router.get("/status")
def health_check() -> dict:
    return {"status": 200, "message": "API is healthy!"}


@router.get("/convert", response_model=ConvertResponse)
def convert(
    from_currency: str = Query(..., min_length=3, max_length=3),
    to_currency: str = Query(..., min_length=3, max_length=3),
    amount: Decimal = Query(gt=0, decimal_places=2),
    service: ExchangeService = Depends(ExchangeService),
) -> ConvertResponse:
    result = service.convert(from_currency, to_currency, amount)
    return ConvertResponse(amount=amount, result=result)
