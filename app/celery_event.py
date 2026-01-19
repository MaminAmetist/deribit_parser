from celery import Celery

celery_app = Celery(
    "deribit_parser",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

# celery_app.autodiscover_tasks(["app.tasks"])

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    worker_pool="solo",
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.fetch_prices.fetch_prices",
        "schedule": 60.0,
    }
}

from app.tasks import fetch_prices
