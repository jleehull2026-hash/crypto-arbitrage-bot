from dataclasses import dataclass
from datetime import datetime


@dataclass
class Opportunity:
    symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    spread: float
    spread_percent: float
    timestamp: datetime

    def to_record(self):
        return {
            "symbol": self.symbol,
            "buy_exchange": self.buy_exchange,
            "sell_exchange": self.sell_exchange,
            "buy_price": self.buy_price,
            "sell_price": self.sell_price,
            "spread": self.spread,
            "spread_percent": self.spread_percent,
            "timestamp": self.timestamp.isoformat(),
        }
