import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str = "arbitrage_bot_data.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    buy_exchange TEXT NOT NULL,
                    sell_exchange TEXT NOT NULL,
                    buy_price REAL NOT NULL,
                    sell_price REAL NOT NULL,
                    spread REAL NOT NULL,
                    spread_percent REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def save_opportunity(self, opportunity):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO opportunities (
                    symbol, buy_exchange, sell_exchange, buy_price, sell_price, spread, spread_percent, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    opportunity.symbol,
                    opportunity.buy_exchange,
                    opportunity.sell_exchange,
                    opportunity.buy_price,
                    opportunity.sell_price,
                    opportunity.spread,
                    opportunity.spread_percent,
                    opportunity.timestamp.isoformat(),
                ),
            )
            conn.commit()

    def get_recent(self, limit: int = 10):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT symbol, buy_exchange, sell_exchange, buy_price, sell_price, spread, spread_percent, timestamp
                FROM opportunities
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return rows
