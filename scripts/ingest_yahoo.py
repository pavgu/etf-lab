#!/usr/bin/env python3
"""ETF data ingestion script using new class-based architecture."""

import sys
from etf.data.ingestion import YahooFinanceIngester


if __name__ == "__main__":
    TICKERS = [
        "SPY",
        "VEA",
        "VWO",
        "SXR8.DE",
    ]
    
    # Check if --full flag is passed for full reload
    full_reload = "--full" in sys.argv
    
    ingester = YahooFinanceIngester()
    ingester.ingest_tickers(TICKERS, incremental=not full_reload)
    
    if full_reload:
        print("\nFull reload completed.")
    else:
        print("\nIncremental update completed. Use --full for complete reload.")
