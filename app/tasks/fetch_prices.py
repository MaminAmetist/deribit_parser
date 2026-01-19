import asyncio

from app import CurrencyTicker
from app.celery_event import celery_app
from app.services.deribit import save_prices

TICKERS = tuple(CurrencyTicker.list())


@celery_app.task
def fetch_prices() -> None:
    """
    Celery-задача для получения цен индексов из Deribit и сохранения их в БД.
    """
    asyncio.run(save_prices(TICKERS))
