import sys
import os
import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from typing import Callable

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


# Import the real app and ExchangeRateService from the module under test.
from main import app as real_app, ExchangeService as RealExchangeRateService


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    TestClient fixture that can be imported across test modules.
    By default it uses the real app. Tests that need to override dependencies
    should use monkeypatch or dependency_overrides in their own fixtures.
    """
    return TestClient(real_app)


@pytest.fixture
def mock_service_factory(
    request, monkeypatch
) -> Callable[[Callable[..., Decimal]], None]:
    """
    Factory fixture: given a function convert_fn(from_currency, to_currency, amount)
    it will patch the ExchangeRateService dependency used by the app so the endpoint
    uses the provided convert_fn and returns Decimal result.
    Usage:
        def convert_fn(f,t,a): return Decimal("12.34")
        mock_service_factory(convert_fn)
    """

    def _patch(convert_fn: Callable[[str, str, Decimal], Decimal]):
        class MockService:
            def convert(
                self, from_currency: str, to_currency: str, amount: Decimal
            ) -> Decimal:
                return convert_fn(from_currency, to_currency, amount)

        # Patch the dependency in the FastAPI app so Depends(ExchangeRateService) yields MockService
        real_app.dependency_overrides[RealExchangeRateService] = lambda: MockService()

        # Ensure teardown after test runs
        def _teardown():
            real_app.dependency_overrides.pop(RealExchangeRateService, None)

        request.addfinalizer(_teardown)

    return _patch
