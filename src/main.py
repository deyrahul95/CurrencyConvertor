from fastapi import FastAPI
from typing import Any

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Exchange Rates
RATES = {
    ("USD", "EUR"): 0.91,
    ("EUR", "USD"): 1.10,
    ("USD", "JPY"): 150.0,
    ("USD", "INR"): 90,
}


@app.get("/status")
def health_check() -> dict:
    return {"status": 200, "message": "API is healthy!"}


@app.get("/convert")
def convert(from_currency: str, to_currency: str, amount: float) -> dict:
    key = (from_currency.upper(), to_currency.upper())
    rate: Any = RATES.get(key)
    logging.info(f"Using exchange rate: {rate}")
    return {"amount": amount, "rate": rate, "result": amount * rate}
