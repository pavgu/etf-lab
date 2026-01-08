#!/usr/bin/env python3
"""Enrich ETF metadata from Yahoo Finance."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import yfinance as yf
from storage.db import get_connection
from storage.schema import ensure_schema
import time

def enrich_metadata():
    ensure_schema()
    con = get_connection()
    
    try:
        # Get all tickers from metadata
        tickers = con.execute("SELECT ticker FROM etf_metadata").fetchall()
        
        print(f"Enriching metadata for {len(tickers)} ETFs...")
        
        for (ticker,) in tickers:
            try:
                print(f"Fetching {ticker}...", end=" ")
                etf = yf.Ticker(ticker)
                info = etf.info
                
                # Extract relevant fields
                long_name = info.get('longName', '')
                category = info.get('category', '')
                fund_family = info.get('fundFamily', '')
                
                # Update description if we got a long name
                if long_name:
                    description = f"{long_name} ({fund_family})" if fund_family else long_name
                    con.execute("""
                        UPDATE etf_metadata 
                        SET description = ?
                        WHERE ticker = ?
                    """, [description, ticker])
                    print(f"✓ {long_name}")
                else:
                    print("✗ No data")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"✗ Error: {e}")
                continue
        
        print("\nMetadata enrichment complete")
        
    finally:
        con.close()

if __name__ == "__main__":
    enrich_metadata()
