from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from models.conversion import Base, ConversionRate


DB_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db_and_seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed data only when empty
    with SessionLocal() as db:
        if not db.execute(select(ConversionRate)).first():
            rates = [
                ConversionRate(
                    from_currency="USD", to_currency="EUR", rate=Decimal("0.924")
                ),
                ConversionRate(
                    from_currency="EUR", to_currency="USD", rate=Decimal("1.082")
                ),
                ConversionRate(
                    from_currency="USD", to_currency="JPY", rate=Decimal("156.84")
                ),
                ConversionRate(
                    from_currency="USD", to_currency="INR", rate=Decimal("90.01")
                ),
                ConversionRate(
                    from_currency="USD", to_currency="GBP", rate=Decimal("0.742")
                ),
                ConversionRate(
                    from_currency="GBP", to_currency="USD", rate=Decimal("1.347")
                ),
                ConversionRate(
                    from_currency="USD", to_currency="AUD", rate=Decimal("1.61")
                ),
                ConversionRate(
                    from_currency="AUD", to_currency="USD", rate=Decimal("0.620")
                ),
                ConversionRate(
                    from_currency="USD", to_currency="CAD", rate=Decimal("1.37")
                ),
                ConversionRate(
                    from_currency="CAD", to_currency="USD", rate=Decimal("0.730")
                ),
            ]
            db.add_all(rates)
            db.commit()
            db.close()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
