import argparse
import time

try:
    from arbitrage_bot.config import settings
    from arbitrage_bot.database import Database
    from arbitrage_bot.exchanges.binance import BinanceExchange
    from arbitrage_bot.exchanges.kucoin import KuCoinExchange
    from arbitrage_bot.logger import logger
    from arbitrage_bot.strategies.spot_arbitrage import SpotArbitrageStrategy
except ImportError:  # pragma: no cover
    from config import settings
    from database import Database
    from exchanges.binance import BinanceExchange
    from exchanges.kucoin import KuCoinExchange
    from logger import logger
    from strategies.spot_arbitrage import SpotArbitrageStrategy


def parse_args():
    parser = argparse.ArgumentParser(description="Crypto arbitrage bot preview")
    parser.add_argument("--once", action="store_true", help="Run a single scan and exit")
    parser.add_argument("--symbol", default=settings.symbol, help="Trading pair to monitor")
    parser.add_argument("--interval", type=int, default=settings.check_interval, help="Seconds between scans")
    parser.add_argument(
        "--min-profit",
        type=float,
        default=settings.min_profit_threshold,
        help="Minimum spread percentage required to trigger an opportunity",
    )
    return parser.parse_args()


def build_strategy(symbol: str, threshold: float):
    buy_exchange = BinanceExchange.build(settings.binance_api_key, settings.binance_api_secret)
    sell_exchange = KuCoinExchange.build(settings.kucoin_api_key, settings.kucoin_api_secret)
    return SpotArbitrageStrategy(buy_exchange, sell_exchange, symbol=symbol, min_profit_threshold=threshold)


def main():
    args = parse_args()
    database = Database(settings.db_path)
    strategy = build_strategy(args.symbol, args.min_profit)

    logger.info("Starting crypto arbitrage monitoring for %s", args.symbol)
    logger.info("Threshold: %.2f%%", args.min_profit)

    if args.once:
        try:
            opp = strategy.scan()
            if opp is None:
                logger.info("No arbitrage opportunity detected")
            else:
                logger.info("Opportunity found: %s", opp)
                database.save_opportunity(opp)
        except Exception as exc:  # pragma: no cover
            logger.exception("Failed to evaluate opportunity: %s", exc)
        return

    try:
        while True:
            try:
                opp = strategy.scan()
                if opp is None:
                    logger.info("No opportunity for %s at %s", args.symbol, args.interval)
                else:
                    logger.info("Opportunity found: %s", opp)
                    database.save_opportunity(opp)
            except Exception as exc:  # pragma: no cover
                logger.exception("Error during arbitrage scan: %s", exc)
            time.sleep(args.interval)
    finally:
        logger.info("Stopping arbitrage bot")


if __name__ == "__main__":
    main()
