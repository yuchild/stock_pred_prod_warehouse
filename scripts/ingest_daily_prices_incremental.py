from __future__ import annotations

import argparse
from datetime import date, timedelta

from src.config.settings import settings
from src.db.price_history_queries import get_max_trade_date
from src.ingestion.load_price_history import load_price_history
from src.ingestion.logging import log_ingestion_result
from src.ingestion.yfinance_client import PriceFetchRequest, fetch_ohlcv


DEFAULT_BACKFILL_DAYS = 5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Incrementally ingest daily stock prices into Postgres."
    )
    parser.add_argument(
        "--symbols",
        type=str,
        default=",".join(settings.default_symbols),
        help="Comma-separated stock symbols",
    )
    parser.add_argument(
        "--interval",
        type=str,
        default="1d",
        help="yfinance interval. Phase 5 expects 1d.",
    )
    parser.add_argument(
        "--backfill-days",
        type=int,
        default=DEFAULT_BACKFILL_DAYS,
        help="Fallback backfill window if no data exists yet.",
    )
    return parser.parse_args()


def determine_request_window(symbol: str, backfill_days: int) -> tuple[date, date]:
    today = date.today()
    max_trade_date = get_max_trade_date(symbol)

    if max_trade_date is None:
        start_date = today - timedelta(days=backfill_days)
    else:
        start_date = max_trade_date - timedelta(days=3)

    end_date = today + timedelta(days=1)
    return start_date, end_date


def main() -> None:
    args = parse_args()
    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]

    total_loaded = 0

    for symbol in symbols:
        start_date, end_date = determine_request_window(
            symbol=symbol,
            backfill_days=args.backfill_days,
        )

        try:
            request = PriceFetchRequest(
                symbol=symbol,
                interval=args.interval,
                period=None,
                start_date=start_date,
                end_date=end_date,
                auto_adjust=False,
            )
            df = fetch_ohlcv(request)
            fetched_rows = len(df)
            loaded_rows = load_price_history(df)
            total_loaded += loaded_rows

            log_ingestion_result(
                pipeline_name="ingest_daily_prices_incremental",
                symbol=symbol,
                interval_code=args.interval,
                request_start_date=start_date,
                request_end_date=end_date,
                row_count_fetched=fetched_rows,
                row_count_loaded=loaded_rows,
                status="SUCCESS",
            )

            print(
                f"{symbol}: start={start_date} end={end_date} "
                f"fetched={fetched_rows} loaded={loaded_rows}"
            )

        except Exception as exc:
            log_ingestion_result(
                pipeline_name="ingest_daily_prices_incremental",
                symbol=symbol,
                interval_code=args.interval,
                request_start_date=start_date,
                request_end_date=end_date,
                row_count_fetched=0,
                row_count_loaded=0,
                status="FAILED",
                error_message=str(exc),
            )
            print(f"{symbol}: FAILED - {exc}")

    print(f"Total loaded rows: {total_loaded}")


if __name__ == "__main__":
    main()