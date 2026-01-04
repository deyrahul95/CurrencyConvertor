from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session


from db.database import get_db
from models.conversion_request import ConversionRequest
from models.conversion_result import ConversionResult
from models.convert_response import ConvertResponse
from services.exchange_rate_service import ExchangeRateService
from services.exchange_service import ExchangeService

router = APIRouter()


def get_exchange_rate_service(db: Session = Depends(get_db)):
    yield ExchangeRateService(db)


@router.get("/health")
def health() -> dict:
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


@router.post("/convert", response_model=ConversionResult)
def convert_post(
    body: ConversionRequest,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
) -> ConversionResult:
    return service.convert(body)
