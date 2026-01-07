#!/usr/bin/env python3
"""Database check script using new class-based architecture."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from etf.data.repository import PriceRepository


def main():
    """Check database contents."""
    try:
        repo = PriceRepository()
        
        # Check row counts and cache data
        tickers = repo.get_available_tickers()
        if not tickers:
            print("No data found in database.")
            return
        
        # Load data once and cache it
        ticker_data = {}
        print("Row counts by ticker:")
        for ticker in tickers:
            df = repo.load_prices(ticker)
            ticker_data[ticker] = df
            print(f"  {ticker}: {len(df)}")
        
        # Show recent data using cached data
        print("\nRecent data (last 5 records):")
        for ticker in list(ticker_data.keys())[:3]:  # Show only first 3 tickers
            df = ticker_data[ticker]
            if not df.empty:
                recent = df.tail(5)
                print(f"\n{ticker}:")
                for _, row in recent.iterrows():
                    print(f"  {row['date'].date()} ${row['close']:.2f}")
    
    except Exception as e:
        print(f"Error checking database: {e}")


if __name__ == "__main__":
    main()