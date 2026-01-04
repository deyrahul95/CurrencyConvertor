from pydantic import BaseModel
from decimal import Decimal


class ConversionResult(BaseModel):
    amount: Decimal
    result: Decimal
    rate: Decimal