from pydantic import BaseModel
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from decimal import Decimal
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Conversion(Base):
    __tablename__ = "conversions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_currency: Mapped[str] = mapped_column(String(length=3))
    to_currency: Mapped[str] = mapped_column(String(length=3))
    rate: Mapped[Decimal] = mapped_column()
    amount: Mapped[Decimal] = mapped_column()
    result: Mapped[Decimal] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)


class ConversionRate(Base):
    __tablename__ = "conversion_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_currency: Mapped[str] = mapped_column(String(length=3))
    to_currency: Mapped[str] = mapped_column(String(length=3))
    rate: Mapped[Decimal] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)


class ConversionResult(BaseModel):
    amount: Decimal
    result: Decimal
    rate: Decimal