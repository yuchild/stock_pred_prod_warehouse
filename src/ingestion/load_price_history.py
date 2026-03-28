from __future__ import annotations

from typing import Iterable

import pandas as pd
from sqlalchemy import text

from src.db.connection import get_engine


UPSERT_SQL = text(
    """
    INSERT INTO raw.stock_price_daily (
        symbol,
        trade_date,
        open_price,
        high_price,
        low_price,
        close_price,
        adj_close_price,
        volume,
        data_source
    )
    VALUES (
        :symbol,
        :trade_date,
        :open_price,
        :high_price,
        :low_price,
        :close_price,
        :adj_close_price,
        :volume,
        :data_source
    )
    ON CONFLICT (symbol, trade_date)
    DO UPDATE SET
        open_price = EXCLUDED.open_price,
        high_price = EXCLUDED.high_price,
        low_price = EXCLUDED.low_price,
        close_price = EXCLUDED.close_price,
        adj_close_price = EXCLUDED.adj_close_price,
        volume = EXCLUDED.volume,
        data_source = EXCLUDED.data_source
    """
)


def _records_from_df(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []

    required_columns = [
        "symbol",
        "trade_date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adj_close_price",
        "volume",
        "data_source",
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    records = df[required_columns].to_dict(orient="records")
    return records


def load_price_history(df: pd.DataFrame) -> int:
    records = _records_from_df(df)
    if not records:
        return 0

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(UPSERT_SQL, records)

    return len(records)


def load_multiple_price_frames(frames: Iterable[pd.DataFrame]) -> int:
    total_rows = 0
    for df in frames:
        total_rows += load_price_history(df)
    return total_rows