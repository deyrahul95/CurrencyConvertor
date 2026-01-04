from decimal import Decimal
from fastapi import FastAPI, Depends, Query
import logging


from convert_response import ConvertResponse
from exchange_rate_service import ExchangeRateService

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/status")
def health_check() -> dict:
    return {"status": 200, "message": "API is healthy!"}


@app.get("/convert")
def convert(
    from_currency: str = Query(str, min_length=3, max_length=3),
    to_currency: str = Query(str, min_length=3, max_length=3),
    amount: Decimal = Query(Decimal, decimal_places=2, gt=0),
    service: ExchangeRateService = Depends(ExchangeRateService),
) -> ConvertResponse:
    result = service.convert(from_currency, to_currency, amount)
    return ConvertResponse(amount=amount, result=result)
