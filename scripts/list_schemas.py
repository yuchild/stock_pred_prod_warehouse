from sqlalchemy import text

from src.db.connection import get_engine


def main() -> None:
    engine = get_engine()

    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name IN ('raw', 'staging', 'mart', 'analytics', 'ml')
                ORDER BY schema_name
                """
            )
        ).fetchall()

    for row in rows:
        print(row[0])


if __name__ == "__main__":
    main()