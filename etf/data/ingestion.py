import time
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


class YahooFinanceIngester:
    """Yahoo Finance data ingester."""
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
    
    def fetch_prices(self, ticker: str, period: str = "10y", start_date: str = None) -> pd.DataFrame:
        """Fetch price data from Yahoo Finance."""
        try:
            params = {
                'ticker': ticker,
                'auto_adjust': False,
                'progress': False,
            }
            
            if start_date:
                params['start'] = start_date
            else:
                params['period'] = period
                
            df = yf.download(**params)

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
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()
    
    def ingest_tickers(self, tickers: list[str], incremental: bool = True):
        """Ingest multiple tickers with optional incremental loading."""
        from etf.data.repository import PriceRepository
        
        repo = PriceRepository()
        
        for ticker in tickers:
            print(f"Ingesting {ticker}...")
            
            start_date = None
            if incremental:
                latest_date = repo.get_latest_date(ticker)
                if latest_date:
                    # Start from day after latest date
                    start_date = (datetime.fromisoformat(latest_date) + timedelta(days=1)).strftime("%Y-%m-%d")
                    print(f"  Starting from {start_date}")
            
            df = self.fetch_prices(ticker, start_date=start_date)

            if df.empty:
                print(f"  ⚠ no new data")
                continue

            repo.save_prices(df)
            print(f"  ✓ {len(df)} rows")
            time.sleep(self.delay)