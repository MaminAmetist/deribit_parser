from enum import Enum


class CurrencyTicker(str, Enum):
    BTC = "BTC"
    ETH = "ETH"

    @classmethod
    def list(cls):
        return [c.value for c in cls]
