from __future__ import annotations

import argparse

from src.config.settings import settings
from src.ingestion.load_price_history import load_multiple_price_frames
from src.ingestion.yfinance_client import PriceFetchRequest, fetch_ohlcv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest daily stock prices into Postgres.")
    parser.add_argument(
        "--symbols",
        type=str,
        default=",".join(settings.default_symbols),
        help="Comma-separated stock symbols, e.g. SPY,QQQ,NVDA",
    )
    parser.add_argument(
        "--period",
        type=str,
        default="2y",
        help="yfinance period, e.g. 1mo, 6mo, 1y, 2y, 5y, max",
    )
    parser.add_argument(
        "--interval",
        type=str,
        default="1d",
        help="yfinance interval. Phase 4 expects 1d.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    symbols = [symbol.strip().upper() for symbol in args.symbols.split(",") if symbol.strip()]
    frames = []

    for symbol in symbols:
        request = PriceFetchRequest(
            symbol=symbol,
            period=args.period,
            interval=args.interval,
            auto_adjust=False,
        )
        df = fetch_ohlcv(request)
        print(f"{symbol}: fetched {len(df)} rows")
        frames.append(df)

    loaded_rows = load_multiple_price_frames(frames)
    print(f"Loaded {loaded_rows} rows into raw.stock_price_daily")


if __name__ == "__main__":
    main()