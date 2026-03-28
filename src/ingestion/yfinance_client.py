from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import yfinance as yf


@dataclass
class PriceFetchRequest:
    symbol: str
    period: str = "2y"
    interval: str = "1d"
    auto_adjust: bool = False


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten yfinance MultiIndex columns when present.
    Keeps the first level for standard OHLCV fields.
    Example:
        ('Open', 'SPY') -> 'Open'
    """
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    return df


def fetch_ohlcv(request: PriceFetchRequest) -> pd.DataFrame:
    """
    Fetch OHLCV data from yfinance and return a standardized DataFrame.

    Output columns:
        symbol
        trade_date
        open_price
        high_price
        low_price
        close_price
        adj_close_price
        volume
        data_source
    """
    df = yf.download(
        tickers=request.symbol,
        period=request.period,
        interval=request.interval,
        auto_adjust=request.auto_adjust,
        progress=False,
        threads=False,
    )

    if df.empty:
        return pd.DataFrame(
            columns=[
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
        )

    df = _flatten_columns(df)
    df = df.reset_index().copy()

    if "Date" in df.columns:
        date_col = "Date"
    elif "Datetime" in df.columns:
        date_col = "Datetime"
    else:
        raise ValueError(
            f"Expected Date or Datetime column for symbol={request.symbol}, "
            f"got columns={list(df.columns)}"
        )

    df["trade_date"] = pd.to_datetime(df[date_col]).dt.date

    # Standardize expected columns
    expected_price_columns = ["Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in expected_price_columns if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing expected OHLCV columns for symbol={request.symbol}: {missing}. "
            f"Available columns: {list(df.columns)}"
        )

    if "Adj Close" not in df.columns:
        df["Adj Close"] = df["Close"]

    standardized = pd.DataFrame(
        {
            "symbol": request.symbol.upper(),
            "trade_date": df["trade_date"],
            "open_price": pd.to_numeric(df["Open"], errors="coerce"),
            "high_price": pd.to_numeric(df["High"], errors="coerce"),
            "low_price": pd.to_numeric(df["Low"], errors="coerce"),
            "close_price": pd.to_numeric(df["Close"], errors="coerce"),
            "adj_close_price": pd.to_numeric(df["Adj Close"], errors="coerce"),
            "volume": pd.to_numeric(df["Volume"], errors="coerce").fillna(0).astype("int64"),
            "data_source": "yfinance",
        }
    )

    standardized = (
        standardized.sort_values("trade_date")
        .drop_duplicates(subset=["symbol", "trade_date"], keep="last")
        .reset_index(drop=True)
    )

    return standardized