from datetime import datetime

from pydantic import BaseModel


class PriceRead(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: datetime

    class Config:
        from_attributes = True
