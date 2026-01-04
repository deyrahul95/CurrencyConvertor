from decimal import Decimal
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address


from db.database import get_db
from models.conversion_request import ConversionRequest
from models.conversion_result import ConversionResult
from models.convert_response import ConvertResponse
from services.exchange_rate_service import ExchangeRateService
from services.exchange_service import ExchangeService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def get_exchange_rate_service(db: Session = Depends(get_db)):
    yield ExchangeRateService(db)


@router.get("/health")
def health() -> dict:
    return {"status": 200, "message": "API is healthy!"}


@router.get("/convert", response_model=ConvertResponse)
@limiter.limit("5/minute")
def convert(
    request: Request,
    from_currency: str = Query(..., min_length=3, max_length=3),
    to_currency: str = Query(..., min_length=3, max_length=3),
    amount: Decimal = Query(gt=0, decimal_places=2),
    service: ExchangeService = Depends(ExchangeService),
) -> ConvertResponse:
    result = service.convert(from_currency, to_currency, amount)
    return ConvertResponse(amount=amount, result=result)


@router.post("/convert", response_model=ConversionResult)
@limiter.limit("5/minute")
def convert_post(
    request: Request,
    body: ConversionRequest,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
) -> ConversionResult:
    return service.convert(body)
