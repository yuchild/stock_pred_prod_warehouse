from dataclasses import dataclass, field
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


@dataclass
class Settings:
    project_name: str = os.getenv("PROJECT_NAME", "stock_pred_prod_warehouse")
    environment: str = os.getenv("ENVIRONMENT", "dev")

    postgres_host: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "stock_pred")
    postgres_user: str = os.getenv("POSTGRES_USER", "stock_user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "change_me")

    airflow_home: str = os.getenv("AIRFLOW_HOME", "./airflow")

    default_symbols: list[str] = field(
        default_factory=lambda: [
            symbol.strip()
            for symbol in os.getenv(
                "DEFAULT_SYMBOLS", "SPY,QQQ,NVDA,AAPL,MSFT"
            ).split(",")
            if symbol.strip()
        ]
    )

    default_interval: str = os.getenv("DEFAULT_INTERVAL", "1d")
    timezone: str = os.getenv("TIMEZONE", "America/Los_Angeles")

    @property
    def sqlalchemy_url(self):
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )


settings = Settings()