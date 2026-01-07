#!/usr/bin/env python3
"""ETF data ingestion script."""

import sys
import pandas as pd
from pathlib import Path
from etf.data.ingestion import YahooFinanceIngester


def load_tickers_from_csv(csv_path: str) -> list[str]:
    """Load ticker symbols from CSV file."""
    try:
        df = pd.read_csv(csv_path)
        if 'symbol' not in df.columns:
            raise ValueError(f"CSV file {csv_path} missing 'symbol' column")
        return df['symbol'].tolist()
    except Exception as e:
        print(f"Error loading CSV file {csv_path}: {e}")
        raise


if __name__ == "__main__":
    full_reload = "--full" in sys.argv
    
    # Determine which CSV to use
    if "--ucits" in sys.argv:
        csv_path = Path("data/universes/universe_ucits_eu_core_v1.csv")
        universe_name = "UCITS"
    elif "--us" in sys.argv:
        csv_path = Path("data/universes/universe_global_etf_core_v2_200.csv")
        universe_name = "US ETFs"
    else:
        # Default tickers for testing
        tickers = ["SPY", "VEA", "VWO"]
        universe_name = "Default"
        csv_path = None
    
    if csv_path:
        if csv_path.exists():
            tickers = load_tickers_from_csv(csv_path)
            print(f"Loaded {len(tickers)} {universe_name} tickers from CSV")
        else:
            print(f"CSV file not found: {csv_path}")
            sys.exit(1)
    
    print(f"Ingesting {len(tickers)} tickers...")
    
    ingester = YahooFinanceIngester()
    ingester.ingest_tickers(tickers, incremental=not full_reload)
    
    if full_reload:
        print("\nFull reload completed.")
    else:
        print("\nIncremental update completed. Use --full for complete reload.")