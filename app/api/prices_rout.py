from datetime import date

from fastapi import APIRouter, Depends, Query

from app import CurrencyTicker
from app.api.prices import get_price_controller, PriceController
from app.shemas.price import PriceRead

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/", response_model=list[PriceRead])
async def get_prices(
        ticker: CurrencyTicker = Query(..., description="Тикер валюты"),
        controller: PriceController = Depends(get_price_controller),
):
    return await controller.get_prices(ticker)


@router.get("/latest", response_model=PriceRead | None)
async def get_latest_price(
        ticker: CurrencyTicker = Query(..., description="Тикер валюты"),
        controller: PriceController = Depends(get_price_controller),
):
    return await controller.get_latest_price(ticker)


@router.get("/by_date", response_model=list[PriceRead])
async def get_prices_by_date(
        ticker: CurrencyTicker = Query(..., description="Тикер валюты"),
        from_date: date | None = Query(None, description="Дата начала (YYYY-MM-DD)"),
        to_date: date | None = Query(None, description="Дата окончания (YYYY-MM-DD)"),
        controller: PriceController = Depends(get_price_controller),
):
    return await controller.get_prices_by_date(
        ticker=ticker,
        from_date=from_date,
        to_date=to_date,
    )
