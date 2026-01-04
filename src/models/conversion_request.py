from pydantic import BaseModel
from decimal import Decimal

from fastapi import Body


class ConversionRequest(BaseModel):
    from_currency: str = Body(..., min_length=3, max_length=3)
    to_currency: str = Body(..., min_length=3, max_length=3)
    amount: Decimal = Body(..., gt=0)