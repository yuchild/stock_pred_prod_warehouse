from sqlalchemy import text

from src.db.connection import get_engine


def main() -> None:
    engine = get_engine()

    query = text(
        """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema IN ('raw', 'staging', 'mart', 'analytics', 'ml')
          AND table_type = 'BASE TABLE'
        ORDER BY table_schema, table_name
        """
    )

    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()

    for schema_name, table_name in rows:
        print(f"{schema_name}.{table_name}")


if __name__ == "__main__":
    main()