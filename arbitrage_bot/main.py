"""Crypto Arbitrage Bot - Main Entry Point"""

import ccxt
import json
from datetime import datetime


def fetch_prices(symbol="BTC/USDT"):
    """Fetch BTC/USDT price from Binance and KuCoin"""
    try:
        binance = ccxt.binance()
        kucoin = ccxt.kucoin()
        
        binance_ticker = binance.fetch_ticker(symbol)
        kucoin_ticker = kucoin.fetch_ticker(symbol)
        
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "binance": {
                "bid": binance_ticker["bid"],
                "ask": binance_ticker["ask"],
                "last": binance_ticker["last"]
            },
            "kucoin": {
                "bid": kucoin_ticker["bid"],
                "ask": kucoin_ticker["ask"],
                "last": kucoin_ticker["last"]
            }
        }
    except Exception as e:
        return {"error": str(e)}


def find_arbitrage(prices):
    """Find arbitrage opportunity"""
    if "error" in prices:
        print(f"Error: {prices['error']}")
        return
    
    binance_ask = prices["binance"]["ask"]
    kucoin_bid = prices["kucoin"]["bid"]
    
    spread = kucoin_bid - binance_ask
    spread_percent = (spread / binance_ask) * 100
    
    print(f"\n{prices['symbol']} - {prices['timestamp']}")
    print(f"Binance Ask: ${binance_ask}")
    print(f"KuCoin Bid:  ${kucoin_bid}")
    print(f"Spread: ${spread:.2f} ({spread_percent:.4f}%)")
    
    if spread_percent > 0.1:
        print("✓ Arbitrage opportunity detected!")
    else:
        print("✗ No profitable arbitrage")


if __name__ == "__main__":
    print("Crypto Arbitrage Bot Started")
    print("Fetching prices...")
    
    prices = fetch_prices("BTC/USDT")
    find_arbitrage(prices)
    
    print("\nDone!")
