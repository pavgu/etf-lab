import time
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta


class YahooFinanceIngester:
    """Yahoo Finance data ingester."""
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def fetch_prices(self, ticker: str, period: str = "10y", start_date: str = None) -> pd.DataFrame:
        """Fetch price data from Yahoo Finance."""
        try:
            if start_date:
                df = yf.download(
                    ticker,
                    start=start_date,
                    auto_adjust=False,
                    progress=False,
                )
            else:
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
        except Exception as e:
            self.logger.error(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()
    
    def ingest_tickers(self, tickers: list[str], incremental: bool = True):
        """Ingest multiple tickers with optional incremental loading."""
        from etf.data.repository import PriceRepository
        
        if not tickers:
            self.logger.warning("No tickers provided for ingestion")
            return
        
        repo = PriceRepository()
        success_count = 0
        
        for ticker in tickers:
            try:
                self.logger.info(f"Ingesting {ticker}...")
                
                start_date = None
                if incremental:
                    latest_date = repo.get_latest_date(ticker)
                    if latest_date:
                        # Convert to string if it's not already
                        if not isinstance(latest_date, str):
                            latest_date = str(latest_date)
                        # Start from day after latest date
                        start_date = (datetime.fromisoformat(latest_date) + timedelta(days=1)).strftime("%Y-%m-%d")
                        self.logger.info(f"  Starting from {start_date}")
                
                df = self.fetch_prices(ticker, start_date=start_date)

                if df.empty:
                    self.logger.warning(f"  No new data for {ticker}")
                    continue

                repo.save_prices(df)
                self.logger.info(f"  ✓ {len(df)} rows saved for {ticker}")
                success_count += 1
                
                if self.delay > 0:
                    time.sleep(self.delay)
                
            except Exception as e:
                self.logger.error(f"Failed to ingest {ticker}: {e}")
                continue
        
        self.logger.info(f"Ingestion completed: {success_count}/{len(tickers)} tickers successful")