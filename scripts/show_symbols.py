from sqlalchemy import text

from src.db.connection import get_engine


def main() -> None:
    engine = get_engine()

    query = text(
        """
        SELECT symbol_id, symbol, asset_type, exchange, currency, is_active
        FROM mart.dim_symbol
        ORDER BY symbol
        """
    )

    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()