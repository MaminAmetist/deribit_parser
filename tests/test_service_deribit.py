from decimal import Decimal

import pytest

from app.services.deribit import fetch_index_price


@pytest.mark.asyncio
async def test_fetch_index_price_success(monkeypatch):
    class DummySession:
        async def get(self, *args, **kwargs):
            class Resp:
                async def json(self):
                    return {"result": {"index_price": 123.456}}

                def raise_for_status(self):
                    return None

            return Resp()

    price = await fetch_index_price(DummySession(), "BTC")
    assert isinstance(price, Decimal)
    assert price == Decimal("123.456")


@pytest.mark.asyncio
async def test_fetch_index_price_unsupported(monkeypatch):
    with pytest.raises(ValueError):
        await fetch_index_price(None, "BAD")
