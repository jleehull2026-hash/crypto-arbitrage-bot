import ccxt

from arbitrage_bot.exchanges.base import BaseExchange


class BinanceExchange(BaseExchange):
    name = "binance"

    @classmethod
    def build(cls, api_key: str = "", api_secret: str = ""):
        exchange = ccxt.binance({"apiKey": api_key, "secret": api_secret, "enableRateLimit": True})
        return cls(exchange)
