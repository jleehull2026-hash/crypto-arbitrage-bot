import ccxt

from arbitrage_bot.exchanges.base import BaseExchange


class KuCoinExchange(BaseExchange):
    name = "kucoin"

    @classmethod
    def build(cls, api_key: str = "", api_secret: str = ""):
        exchange = ccxt.kucoin({"apiKey": api_key, "secret": api_secret, "enableRateLimit": True})
        return cls(exchange)
