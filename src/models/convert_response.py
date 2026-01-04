from pydantic import BaseModel, Field, model_validator
from decimal import Decimal


class ConvertResponse(BaseModel):
    amount: Decimal = Field(..., gt=0)
    result: Decimal = Field(..., gt=0)
    rate: Decimal = Field(default=Decimal(0))

    @model_validator(mode="after")
    def set_rate(self):
        self.rate = (self.result / self.amount).quantize(Decimal("0.01"))
        return self
