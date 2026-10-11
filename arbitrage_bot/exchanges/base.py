from abc import ABC, abstractmethod


class BaseExchange(ABC):
    name = "base"

    def __init__(self, client):
        self.client = client

    def get_ticker(self, symbol: str):
        ticker = self.client.fetch_ticker(symbol)
        return {
            "symbol": symbol,
            "bid": float(ticker["bid"]),
            "ask": float(ticker["ask"]),
            "last": float(ticker.get("last", 0.0)),
        }

    @classmethod
    @abstractmethod
    def build(cls, api_key: str = "", api_secret: str = ""):
        raise NotImplementedError
