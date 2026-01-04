from decimal import Decimal
import logging
from fastapi import HTTPException


class ExchangeRateService:
    __RATES: dict[tuple[str, str], Decimal] = {
        ("USD", "EUR"): Decimal(0.924),
        ("EUR", "USD"): Decimal(1.082),
        ("USD", "JPY"): Decimal(156.84),
        ("USD", "INR"): Decimal(90.01),
        ("USD", "GBP"): Decimal(0.742),
        ("GBP", "USD"): Decimal(1.347),
        ("USD", "AUD"): Decimal(1.61),
        ("AUD", "USD"): Decimal(0.620),
        ("USD", "CAD"): Decimal(1.37),
        ("CAD", "USD"): Decimal(0.730),
    }

    def convert(self, from_currency: str, to_currency: str, amount: Decimal) -> Decimal:
        key = (from_currency.upper(), to_currency.upper())
        rate = self.__RATES.get(key)

        if rate is None:
            raise HTTPException(
                status_code=404,
                detail=f"Exchange rate from {from_currency} to {to_currency} is not available.",
            )

        logging.info(f"Using exchange rate: {rate}")
        return amount * rate
