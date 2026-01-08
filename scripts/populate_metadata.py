#!/usr/bin/env python3
"""Populate ETF metadata from universe CSV files."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from storage.db import get_connection
from storage.schema import ensure_schema

def populate_metadata():
    ensure_schema()
    con = get_connection()
    
    try:
        # Load US ETFs
        us_file = project_root / "data/universes/universe_global_etf_core_v2_200.csv"
        if us_file.exists():
            df = pd.read_csv(us_file)
            for _, row in df.iterrows():
                con.execute("""
                    INSERT OR REPLACE INTO etf_metadata 
                    (ticker, isin, asset_class, region, category, currency, exchange)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, [row['symbol'], row.get('isin'), row['asset_class'], 
                      row['region'], row['category'], row['currency'], row['exchange']])
            print(f"Loaded {len(df)} US ETFs")
        
        # Load UCITS ETFs
        ucits_file = project_root / "data/universes/universe_ucits_eu_core_v1.csv"
        if ucits_file.exists():
            df = pd.read_csv(ucits_file)
            for _, row in df.iterrows():
                con.execute("""
                    INSERT OR REPLACE INTO etf_metadata 
                    (ticker, isin, asset_class, region, category, currency, exchange)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, [row['symbol'], row.get('isin'), row['asset_class'], 
                      row['region'], row['category'], row['currency'], row['exchange']])
            print(f"Loaded {len(df)} UCITS ETFs")
        
        print("Metadata population complete")
        
    finally:
        con.close()

if __name__ == "__main__":
    populate_metadata()
