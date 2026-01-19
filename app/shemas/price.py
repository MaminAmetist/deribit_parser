from pydantic import BaseModel
from datetime import datetime


class PriceRead(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: datetime

    class Config:
        from_attributes = True  # Позволяет Pydantic читать данные прямо из объектов SQLAlchemy
