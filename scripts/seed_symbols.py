from sqlalchemy import text

from src.config.settings import settings
from src.db.connection import get_engine


def main() -> None:
    engine = get_engine()

    insert_sql = text(
        """
        INSERT INTO mart.dim_symbol (symbol, asset_type, exchange, currency, is_active)
        VALUES (:symbol, :asset_type, :exchange, :currency, :is_active)
        ON CONFLICT (symbol) DO UPDATE
        SET
            asset_type = EXCLUDED.asset_type,
            exchange = EXCLUDED.exchange,
            currency = EXCLUDED.currency,
            is_active = EXCLUDED.is_active,
            updated_at = NOW()
        """
    )

    rows = [
        {
            "symbol": symbol,
            "asset_type": "equity",
            "exchange": "unknown",
            "currency": "USD",
            "is_active": True,
        }
        for symbol in settings.default_symbols
    ]

    with engine.begin() as conn:
        conn.execute(insert_sql, rows)

    print(f"Upserted {len(rows)} symbols into mart.dim_symbol")


if __name__ == "__main__":
    main()