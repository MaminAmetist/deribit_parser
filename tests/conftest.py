from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient, ASGITransport

from app.api.prices import PriceController
from app.main import app


@pytest.fixture
def mock_session():
    session = AsyncMock()
    return session


@pytest.fixture
def fake_prices():
    p1 = MagicMock(timestamp=100, ticker="BTC")
    p2 = MagicMock(timestamp=200, ticker="BTC")
    return [p1, p2]


@pytest.fixture
def controller(mock_session):
    return PriceController(session=mock_session)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
            transport=transport,
            base_url="http://test",
    ) as client:
        yield client
