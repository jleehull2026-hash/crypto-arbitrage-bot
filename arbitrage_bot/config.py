from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


@dataclass
class Settings:
    symbol: str = os.getenv("ARBITRAGE_SYMBOL", "BTC/USDT")
    check_interval: int = int(os.getenv("CHECK_INTERVAL_SECONDS", "5"))
    min_profit_threshold: float = float(os.getenv("MIN_PROFIT_THRESHOLD", "0.1"))
    db_path: str = os.getenv("DATABASE_PATH", str(BASE_DIR / "arbitrage_bot_data.db"))
    binance_api_key: str = os.getenv("BINANCE_API_KEY", "")
    binance_api_secret: str = os.getenv("BINANCE_API_SECRET", "")
    kucoin_api_key: str = os.getenv("KUCOIN_API_KEY", "")
    kucoin_api_secret: str = os.getenv("KUCOIN_API_SECRET", "")
    gate_api_key: str = os.getenv("GATE_API_KEY", "")
    gate_api_secret: str = os.getenv("GATE_API_SECRET", "")


settings = Settings()
