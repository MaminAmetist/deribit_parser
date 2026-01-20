from fastapi import FastAPI
from app.api.prices_rout import router as prices_router

app = FastAPI(
    title="Crypto Price Service",
    version="0.1.0",
)

app.include_router(prices_router)
