from decimal import Decimal

import pytest

from app.services.deribit import fetch_index_price


class DummyResponse:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def json(self):
        return {"result": {"index_price": 123.456}}

    def raise_for_status(self):
        return None


class DummySession:
    def get(self, *args, **kwargs):
        return DummyResponse()


@pytest.mark.asyncio
async def test_fetch_index_price_success():
    price = await fetch_index_price(DummySession(), "BTC")

    assert price == Decimal("123.456")
