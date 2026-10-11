from datetime import datetime

from arbitrage_bot.models import Opportunity


class SpotArbitrageStrategy:
    def __init__(self, buy_exchange, sell_exchange, symbol: str, min_profit_threshold: float = 0.1):
        self.buy_exchange = buy_exchange
        self.sell_exchange = sell_exchange
        self.symbol = symbol
        self.min_profit_threshold = min_profit_threshold

    def scan(self):
        buy_ticker = self.buy_exchange.get_ticker(self.symbol)
        sell_ticker = self.sell_exchange.get_ticker(self.symbol)

        buy_price = float(buy_ticker["ask"])
        sell_price = float(sell_ticker["bid"])
        spread = sell_price - buy_price
        spread_percent = (spread / buy_price) * 100

        if spread_percent <= self.min_profit_threshold:
            return None

        return Opportunity(
            symbol=self.symbol,
            buy_exchange=self.buy_exchange.name,
            sell_exchange=self.sell_exchange.name,
            buy_price=buy_price,
            sell_price=sell_price,
            spread=spread,
            spread_percent=spread_percent,
            timestamp=datetime.utcnow(),
        )
