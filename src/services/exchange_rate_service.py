from datetime import datetime
import logging

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.conversion_request import ConversionRequest
from models.conversion_result import ConversionResult
from models.conversion import Conversion, ConversionRate


class ExchangeRateService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def convert(self, request: ConversionRequest) -> ConversionResult:
        from_currency = request.from_currency.upper()
        to_currency = request.to_currency.upper()

        logging.info(
            f"Searching conversation rate form {from_currency} to {to_currency} currency.."
        )

        conversion_rate = (
            self.db.query(ConversionRate)
            .filter_by(from_currency=from_currency, to_currency=to_currency)
            .order_by(ConversionRate.timestamp.desc())
            .first()
        )

        if conversion_rate is None or conversion_rate.rate is None:
            logging.info(
                f"Conversation rate not found form {from_currency} to {to_currency} currency."
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation rate not found form {request.from_currency} to {request.to_currency} currency.",
            )

        logging.info(
            f"Conversation rate form {from_currency} to {to_currency} currency is {conversion_rate.rate}"
        )
        result = round(request.amount * conversion_rate.rate, 2)

        conversion = Conversion(
            from_currency=request.from_currency,
            to_currency=request.to_currency,
            rate=conversion_rate.rate,
            amount=request.amount,
            result=result,
            timestamp=datetime.now(),
        )
        self.db.add(conversion)
        self.db.commit()

        return ConversionResult(
            amount=request.amount, result=result, rate=round(conversion_rate.rate, 2)
        )
