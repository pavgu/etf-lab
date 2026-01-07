#!/usr/bin/env python3
"""Analyze exchanges from stored ticker data."""

import sys
from pathlib import Path
from collections import Counter

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from etf.data.repository import PriceRepository

def analyze_exchanges():
    repo = PriceRepository()
    tickers = repo.get_available_tickers()
    
    if not tickers:
        print("No tickers found in database.")
        return
    
    # Analyze ticker suffixes to identify exchanges
    exchanges = []
    for ticker in tickers:
        if '.L' in ticker:
            exchanges.append('LSE (London)')
        elif '.DE' in ticker:
            exchanges.append('Xetra (Germany)')
        else:
            exchanges.append('US (NYSE Arca/NASDAQ)')
    
    exchange_counts = Counter(exchanges)
    
    print(f"Total tickers: {len(tickers)}")
    print(f"Exchanges represented:")
    for exchange, count in exchange_counts.items():
        print(f"  {exchange}: {count} tickers")
    
    print(f"\nTotal exchanges: {len(exchange_counts)}")

if __name__ == "__main__":
    analyze_exchanges()