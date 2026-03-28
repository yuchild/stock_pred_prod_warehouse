from __future__ import annotations

from datetime import date
from sqlalchemy import text

from src.db.connection import get_engine


def log_ingestion_result(
    pipeline_name: str,
    symbol: str,
    interval_code: str,
    request_start_date: date | None,
    request_end_date: date | None,
    row_count_fetched: int,
    row_count_loaded: int,
    status: str,
    error_message: str | None = None,
) -> None:
    engine = get_engine()

    stmt = text(
        """
        INSERT INTO analytics.ingestion_log (
            pipeline_name,
            symbol,
            interval_code,
            request_start_date,
            request_end_date,
            row_count_fetched,
            row_count_loaded,
            status,
            error_message,
            finished_at
        )
        VALUES (
            :pipeline_name,
            :symbol,
            :interval_code,
            :request_start_date,
            :request_end_date,
            :row_count_fetched,
            :row_count_loaded,
            :status,
            :error_message,
            NOW()
        )
        """
    )

    with engine.begin() as conn:
        conn.execute(
            stmt,
            {
                "pipeline_name": pipeline_name,
                "symbol": symbol,
                "interval_code": interval_code,
                "request_start_date": request_start_date,
                "request_end_date": request_end_date,
                "row_count_fetched": row_count_fetched,
                "row_count_loaded": row_count_loaded,
                "status": status,
                "error_message": error_message,
            },
        )