from datetime import datetime, date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import CurrencyTicker
from app.core.db_depends import get_async_db
from app.models.price import Price
from app.shemas.price import PriceRead

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/", response_model=list[PriceRead])
async def get_prices(
        ticker: CurrencyTicker = Query(..., description="Тикер валюты"),
        session: AsyncSession = Depends(get_async_db),
):
    """
    Получение всех сохранённых данных по валюте.
    """
    stmt = (
        select(Price)
        .where(Price.ticker == ticker.value)
        .order_by(Price.timestamp)
    )

    result = await session.execute(stmt)
    prices = result.scalars().all()

    return prices


@router.get("/latest", response_model=PriceRead)
async def get_latest_price(
        ticker: CurrencyTicker = Query(..., description="Тикер валюты"),
        session: AsyncSession = Depends(get_async_db),
):
    """
    Получение последней цены валюты.
    """
    stmt = (
        select(Price)
        .where(Price.ticker == ticker.value)
        .order_by(Price.timestamp.desc())
        .limit(1)
    )

    result = await session.execute(stmt)
    price = result.scalar_one_or_none()

    return price


@router.get("/by_date", response_model=list[PriceRead])
async def get_prices_by_date(
        ticker: CurrencyTicker = Query(..., description="Тикер валюты"),
        from_date: date | None = Query(
            None,
            description="Дата начала (YYYY-MM-DD)",
        ),
        to_date: date | None = Query(
            None,
            description="Дата окончания (YYYY-MM-DD)",
        ),
        session: AsyncSession = Depends(get_async_db),
):
    """
    Получение цен по тикеру за диапазон дат.
    """

    stmt = select(Price).where(Price.ticker == ticker.value)

    if from_date is not None:
        from_ts = int(datetime.combine(from_date, datetime.min.time()).timestamp())
        stmt = stmt.where(Price.timestamp >= from_ts)

    if to_date is not None:
        to_ts = int(datetime.combine(to_date, datetime.max.time()).timestamp())
        stmt = stmt.where(Price.timestamp <= to_ts)

    stmt = stmt.order_by(Price.timestamp)

    result = await session.execute(stmt)
    return result.scalars().all()
