from datetime import datetime, date

from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import CurrencyTicker
from app.core.db_depends import get_async_db
from app.models.price import Price


class PriceController:
    """
    Controller for price-related endpoints.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _validate_date_range(
            from_date: date | None,
            to_date: date | None,
    ) -> None:
        """
        Validate date range consistency.
        """
        if from_date and to_date and from_date > to_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="from_date cannot be greater than to_date",
            )

    @staticmethod
    def _validate_not_future(d: date | None) -> None:
        """
        Prevent future dates.
        """
        if d and d > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Date cannot be in the future",
            )

    async def get_prices(
            self,
            ticker: CurrencyTicker,
    ) -> list[Price]:
        """
        Get all stored prices for a ticker.
        """
        stmt = (
            select(Price)
            .where(Price.ticker == ticker.value)
            .order_by(Price.timestamp)
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_latest_price(
            self,
            ticker: CurrencyTicker,
    ) -> Price | None:
        """
        Get latest price for a ticker.
        """
        stmt = (
            select(Price)
            .where(Price.ticker == ticker.value)
            .order_by(Price.timestamp.desc())
            .limit(1)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_prices_by_date(
            self,
            ticker: CurrencyTicker,
            from_date: date | None,
            to_date: date | None,
    ) -> list[Price]:
        """
        Get prices for a ticker within a date range.
        """
        self._validate_date_range(from_date, to_date)
        self._validate_not_future(from_date)
        self._validate_not_future(to_date)

        stmt = select(Price).where(Price.ticker == ticker.value)

        if from_date:
            from_ts = int(
                datetime.combine(from_date, datetime.min.time()).timestamp()
            )
            stmt = stmt.where(Price.timestamp >= from_ts)

        if to_date:
            to_ts = int(
                datetime.combine(to_date, datetime.max.time()).timestamp()
            )
            stmt = stmt.where(Price.timestamp <= to_ts)

        stmt = stmt.order_by(Price.timestamp)

        result = await self._session.execute(stmt)
        return result.scalars().all()


def get_price_controller(
        session: AsyncSession = Depends(get_async_db),
) -> PriceController:
    """
    Dependency factory for PriceController.
    """
    return PriceController(session)
