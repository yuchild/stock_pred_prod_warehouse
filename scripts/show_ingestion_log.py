from sqlalchemy import text

from src.db.connection import get_engine


def main() -> None:
    engine = get_engine()

    query = text(
        """
        SELECT
            ingestion_log_id,
            pipeline_name,
            symbol,
            interval_code,
            request_start_date,
            request_end_date,
            row_count_fetched,
            row_count_loaded,
            status,
            finished_at
        FROM analytics.ingestion_log
        ORDER BY ingestion_log_id DESC
        LIMIT 25
        """
    )

    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()