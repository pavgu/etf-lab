#!/usr/bin/env python3
"""ETF data ingestion script using new class-based architecture."""

import sys
import argparse
from etf.data.ingestion import YahooFinanceIngester


def main():
    parser = argparse.ArgumentParser(description='Ingest ETF data from Yahoo Finance')
    parser.add_argument('--full', action='store_true', help='Full reload of all historical data')
    args = parser.parse_args()
    
    TICKERS = [
        "SPY",
        "VEA",
        "VWO",
        "SXR8.DE",
    ]
    
    try:
        ingester = YahooFinanceIngester()
        ingester.ingest_tickers(TICKERS, incremental=not args.full)
        
        if args.full:
            print("\nFull reload completed.")
        else:
            print("\nIncremental update completed. Use --full for complete reload.")
    except Exception as e:
        print(f"Error during ingestion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
