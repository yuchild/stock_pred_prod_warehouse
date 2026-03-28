from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.config.settings import settings


def get_engine() -> Engine:
    return create_engine(
        settings.sqlalchemy_url,
        pool_pre_ping=True,
        future=True,
    )


def test_connection() -> dict:
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT
                    current_database() AS database_name,
                    current_user AS user_name,
                    version() AS postgres_version
                """
            )
        ).mappings().one()

    return dict(result)
