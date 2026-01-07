#!/usr/bin/env python3
"""Database check script using new class-based architecture."""

from etf.data.repository import PriceRepository


def main():
    """Check database contents."""
    try:
        repo = PriceRepository()
        
        # Check row counts
        tickers = repo.get_available_tickers()
        if not tickers:
            print("No data found in database.")
            return
        
        print("Row counts by ticker:")
        for ticker in tickers:
            df = repo.load_prices(ticker)
            print(f"  {ticker}: {len(df)}")
        
        # Show recent data
        print("\nRecent data (last 5 records):")
        for ticker in tickers[:3]:  # Show only first 3 tickers
            df = repo.load_prices(ticker)
            if not df.empty:
                recent = df.tail(5)
                print(f"\n{ticker}:")
                for _, row in recent.iterrows():
                    print(f"  {row['date'].date()} ${row['close']:.2f}")
    
    except Exception as e:
        print(f"Error checking database: {e}")


if __name__ == "__main__":
    main()