import pytest
from datetime import date

@pytest.mark.asyncio
async def test_get_prices_by_date_empty(async_client):
    response = await async_client.get(
        "/prices/by_date?ticker=BTC&from_date=2025-01-01&to_date=2025-01-02"
    )
    assert response.status_code == 200
    assert response.json() == []

