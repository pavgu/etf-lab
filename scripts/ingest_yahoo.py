import time
import yfinance as yf
import pandas as pd

from storage.db import get_connection
from storage.schema import ensure_schema


def fetch_prices(ticker: str, period="10y") -> pd.DataFrame:
    df = yf.download(
        ticker,
        period=period,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        return df

    df = df.reset_index()
    df.columns = [c[0].lower().replace(" ", "_") if isinstance(c, tuple) else c.lower().replace(" ", "_") for c in df.columns]
    df["ticker"] = ticker

    return df[[
        "ticker", "date",
        "open", "high", "low",
        "close", "adj_close", "volume"
    ]]


def upsert_prices(df: pd.DataFrame):
    con = get_connection()
    con.register("df", df)

    con.execute("""
        INSERT OR REPLACE INTO prices
        SELECT * FROM df
    """)

    con.close()


def ingest(tickers: list[str]):
    ensure_schema()

    for ticker in tickers:
        print(f"Ingesting {ticker}...")
        df = fetch_prices(ticker)

        if df.empty:
            print(f"no data")
            continue

        upsert_prices(df)
        print(f" {len(df)} rows")

        time.sleep(1.0)  # Make a brief pause to avoid rate limiting


if __name__ == "__main__":
    TICKERS = [
        "SPY",
        "VEA",
        "VWO",
        "SXR8.DE",
    ]
    ingest(TICKERS)
