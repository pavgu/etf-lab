import pandas as pd
from storage.db import get_connection
from storage.schema import ensure_schema


class PriceRepository:
    """Repository for price data operations."""
    
    def __init__(self):
        ensure_schema()
    
    def save_prices(self, df: pd.DataFrame):
        """Save price data to database."""
        con = get_connection()
        try:
            con.register("df", df)
            con.execute("""
                INSERT OR REPLACE INTO prices
                SELECT * FROM df
            """)
        finally:
            con.close()
    
    def load_prices(self, ticker: str) -> pd.DataFrame:
        """Load price data for a ticker."""
        con = get_connection()
        try:
            df = pd.read_sql(
                "SELECT * FROM prices WHERE ticker = ? ORDER BY date",
                con, params=[ticker]
            )
            df['date'] = pd.to_datetime(df['date'])
            return df
        finally:
            con.close()
    
    def get_latest_date(self, ticker: str) -> str | None:
        """Get the latest date for a ticker in the database."""
        con = get_connection()
        try:
            result = con.execute(
                "SELECT MAX(date) FROM prices WHERE ticker = ?", 
                [ticker]
            ).fetchone()
            return result[0] if result and result[0] else None
        finally:
            con.close()
    
    def get_available_tickers(self) -> list[str]:
        """Get list of available tickers in database."""
        con = get_connection()
        try:
            result = con.execute("SELECT DISTINCT ticker FROM prices ORDER BY ticker").fetchall()
            return [row[0] for row in result]
        finally:
            con.close()