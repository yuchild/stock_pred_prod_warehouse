from __future__ import annotations

from datetime import date
from sqlalchemy import text

from src.db.connection import get_engine


def get_max_trade_date(symbol: str) -> date | None:
    engine = get_engine()

    query = text(
        """
        SELECT MAX(trade_date) AS max_trade_date
        FROM raw.stock_price_daily
        WHERE symbol = :symbol
        """
    )

    with engine.connect() as conn:
        row = conn.execute(query, {"symbol": symbol.upper()}).mappings().one()

    return row["max_trade_date"]