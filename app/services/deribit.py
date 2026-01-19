from decimal import Decimal

import aiohttp

from app import CurrencyTicker

DERIBIT_URL = "https://www.deribit.com/api/v2/public/get_index_price"

SUPPORTED_INDEXES = {
    ticker.value: f"{ticker.value.lower()}_usd"
    for ticker in CurrencyTicker
}


async def fetch_index_price(
        session: aiohttp.ClientSession,
        ticker: str,
) -> Decimal:
    try:
        index_name = SUPPORTED_INDEXES[ticker.upper()]
    except KeyError:
        raise ValueError(f"Unsupported ticker: {ticker}")

    params = {"index_name": index_name}

    async with session.get(
            DERIBIT_URL,
            params=params,
            timeout=aiohttp.ClientTimeout(total=10),
    ) as resp:
        resp.raise_for_status()
        payload = await resp.json()

    if "result" not in payload or "index_price" not in payload["result"]:
        raise RuntimeError(f"Unexpected Deribit response: {payload}")

    return Decimal(str(payload["result"]["index_price"]))


import aiohttp
import time
from typing import Iterable

from app.core.database import async_session_maker
from app.models.price import Price


async def save_prices(tickers: Iterable[str]) -> None:
    async with aiohttp.ClientSession() as http_session:
        async with async_session_maker() as db_session:
            for ticker in tickers:
                price = await fetch_index_price(http_session, ticker)

                db_session.add(
                    Price(
                        ticker=ticker,
                        price=price,
                        timestamp=int(time.time()),
                    )
                )

            await db_session.commit()
