from datetime import date

from fastapi import APIRouter, Depends, Query

from app import CurrencyTicker
from app.api.prices import PriceController, get_price_controller
from app.schemas.price import PriceRead

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/", response_model=list[PriceRead])
async def get_prices(
        ticker: CurrencyTicker = Query(...),
        controller: PriceController = Depends(get_price_controller),
):
    return await controller.get_prices(ticker)


@router.get("/latest", response_model=PriceRead | None)
async def get_latest_price(
        ticker: CurrencyTicker = Query(...),
        controller: PriceController = Depends(get_price_controller),
):
    return await controller.get_latest_price(ticker)


async def get_prices_by_date(
        ticker: CurrencyTicker = Query(..., description="Тикер валюты"),
        from_date: date | None = Query(
            None,
            description="Дата начала в формате YYYY-MM-DD",
            example="2026-01-01",
        ),
        to_date: date | None = Query(
            None,
            description="Дата окончания в формате YYYY-MM-DD",
            example="2026-01-31",
        ),
        controller: PriceController = Depends(get_price_controller),
):
    return await controller.get_prices_by_date(
        ticker=ticker,
        from_date=from_date,
        to_date=to_date,
    )
