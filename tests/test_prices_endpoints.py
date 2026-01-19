from datetime import date
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import timedelta


import pytest

from app import CurrencyTicker


@pytest.mark.asyncio
async def test_get_prices_returns_list(
    controller,
    mock_session,
    fake_prices,
):
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = fake_prices
    mock_session.execute.return_value = result_mock

    prices = await controller.get_prices(CurrencyTicker.BTC)

    mock_session.execute.assert_called_once()
    assert prices == fake_prices


@pytest.mark.asyncio
async def test_get_latest_price_none(
    controller,
    mock_session,
):
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = result_mock

    price = await controller.get_latest_price(CurrencyTicker.BTC)

    assert price is None



@pytest.mark.asyncio
async def test_get_prices_by_date_success(
    controller,
    mock_session,
    fake_prices,
):
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = fake_prices
    mock_session.execute.return_value = result_mock

    prices = await controller.get_prices_by_date(
        ticker=CurrencyTicker.BTC,
        from_date=date(2024, 1, 1),
        to_date=date(2024, 1, 31),
    )

    assert prices == fake_prices



@pytest.mark.asyncio
async def test_get_prices_by_date_invalid_range(controller):
    with pytest.raises(HTTPException) as exc:
        await controller.get_prices_by_date(
            ticker=CurrencyTicker.BTC,
            from_date=date(2024, 2, 1),
            to_date=date(2024, 1, 1),
        )

    assert exc.value.status_code == 400
    assert "from_date cannot be greater" in exc.value.detail

@pytest.mark.asyncio
async def test_get_prices_by_date_future_date(controller):
    future = date.today() + timedelta(days=1)

    with pytest.raises(HTTPException) as exc:
        await controller.get_prices_by_date(
            ticker=CurrencyTicker.BTC,
            from_date=future,
            to_date=None,
        )

    assert exc.value.status_code == 400
    assert "future" in exc.value.detail.lower()



@pytest.mark.asyncio
async def test_get_prices_by_date_empty_result(
    controller,
    mock_session,
):
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = result_mock

    prices = await controller.get_prices_by_date(
        ticker=CurrencyTicker.BTC,
        from_date=None,
        to_date=None,
    )

    assert prices == []

